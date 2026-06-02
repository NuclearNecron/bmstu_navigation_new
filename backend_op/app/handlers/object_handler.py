import logging

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_handler import BaseHandler
from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.models.object_models import Object
from app.schemas.object_models_schemas import (
    NodeTypeCreateParams,
    ObjectCreateSchema,
    ObjectMapperSchema,
    ObjectSchema,
    ObjectUpdateSchema,
)

log = logging.getLogger(__name__)


class ObjectHandler(BaseHandler[ObjectCreateSchema, ObjectUpdateSchema, ObjectSchema]):
    async def create(
        self, session: AsyncSession, data: ObjectCreateSchema
    ) -> ObjectSchema:
        log.info("Создаём запись Object")
        instance = Object(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ObjectSchema.model_validate(instance)

    async def update(
        self, session: AsyncSession, data: ObjectUpdateSchema
    ) -> ObjectSchema | None:
        log.info("Обновляем запись Object id=%s", data.id)
        instance = await session.get(Object, data.id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True, exclude={"id"}).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ObjectSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity: GetSchema
    ) -> ObjectSchema | None:
        log.info("Получаем запись Object id=%s", entity.id)
        instance = await session.get(Object, entity.id)
        if instance is None:
            return None
        return ObjectSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        log.info("Удаляем запись Object id=%s", entity.id)
        instance = await session.get(Object, entity.id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> list[ObjectSchema]:
        log.info("Получаем все записи Object")
        query = select(Object)
        result = await session.execute(query)
        return [ObjectSchema.model_validate(row) for row in result.scalars().all()]

    async def get_all_for_mapper(
        self, session: AsyncSession
    ) -> list[ObjectMapperSchema]:
        log.info("Получаем все записи Object")
        query = select(Object.id, Object.parent_id)
        result = await session.execute(query)
        return [
            ObjectMapperSchema.model_validate(row) for row in result.scalars().all()
        ]

    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[ObjectSchema]:
        log.info(
            "Получаем записи Object page=%s limit=%s",
            pagination.page,
            pagination.limit,
        )
        query = (
            select(Object)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        result = await session.execute(query)
        return [ObjectSchema.model_validate(row) for row in result.scalars().all()]

    async def get_children_by_parent(
        self, session: AsyncSession, parent_id: int
    ) -> list[ObjectSchema]:
        """
        Получить список дочерних объектов по parent_id.

        Args:
            session: Асинхронная сессия SQLAlchemy
            parent_id: Идентификатор родительского объекта

        Returns:
            Список схем дочерних объектов
        """
        log.info("Получаем дочерние объекты для parent_id=%s", parent_id)
        query = select(Object).where(Object.parent_id == parent_id)
        result = await session.execute(query)
        return [ObjectSchema.model_validate(row) for row in result.scalars().all()]

    async def get_parent_chain(
        self, session: AsyncSession, object_id: int
    ) -> NodeTypeCreateParams:
        log.info("Собираем цепочку родителей для object_id=%s", object_id)
        # Получаем полную цепочку родителей от object_id до uni
        chain = await self._get_parent_chain_recursive(session, object_id)

        if not chain:
            return NodeTypeCreateParams(id=object_id)

        # Собираем структуру NodeTypeCreateParams
        # Проходим по цепочке от object_id до uni и заполняем поля
        result_params = NodeTypeCreateParams(id=object_id)

        # Заполняем поля в зависимости от позиции в цепочке
        # chain[0] - это object_id, chain[-1] - это uni (parent_id is None)
        # Проходим по цепочке и заполняем соответствующие поля
        for i, row in enumerate(chain):
            # Определяем поле по позиции от конца цепочки (uni - это последний)
            # uni - index -1, campus - index -2, complex - index -3, и т.д.
            level_index = len(chain) - 1 - i

            if level_index == 0 and row.parent_id is None:
                # Это uni (самый верхний уровень)
                result_params.uni = row.id
            elif level_index == 1:
                result_params.campus = row.id
            elif level_index == 2:
                result_params.complex = row.id
            elif level_index == 3:
                result_params.corpus = row.id
            elif level_index == 4:
                result_params.building = row.id
            elif level_index == 5:
                result_params.floor = row.id
            elif level_index == 6:
                result_params.transit = row.id
            elif level_index == 7:
                result_params.room = row.id
            elif level_index == 8:
                result_params.exit_point = row.id

        return result_params

    async def _get_parent_chain_recursive(
        self, session: AsyncSession, object_id: int
    ) -> list:
        log.info("Собираем цепочку родителей для object_id=%s", object_id)

        # CTE запрос для получения всей цепочки родителей
        query = text("""
            WITH RECURSIVE parent_chain AS (
                SELECT id, parent_id
                FROM object
                WHERE id = :object_id

                UNION ALL

                SELECT o.id, o.parent_id
                FROM object o
                INNER JOIN parent_chain pc ON o.id = pc.parent_id
            )
            SELECT * FROM parent_chain ORDER BY id
        """)

        result = await session.execute(query, {"object_id": object_id})
        rows = result.fetchall()

        return rows
