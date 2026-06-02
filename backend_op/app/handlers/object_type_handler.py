import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_handler import BaseHandler
from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.models.const_types import ObjectType
from app.schemas.const_types_schemas import (
    ObjectTypeCreateSchema,
    ObjectTypeEditSchema,
    ObjectTypeSchema,
)

log = logging.getLogger(__name__)


class ObjectTypeHandler(
    BaseHandler[ObjectTypeCreateSchema, ObjectTypeEditSchema, ObjectTypeSchema]
):
    async def create(
        self, session: AsyncSession, data: ObjectTypeCreateSchema
    ) -> ObjectTypeSchema:
        log.info("Создаём запись ObjectType")
        instance = ObjectType(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ObjectTypeSchema.model_validate(instance)

    async def update(
        self, session: AsyncSession, data: ObjectTypeEditSchema
    ) -> ObjectTypeSchema | None:
        log.info("Обновляем запись ObjectType id=%s", data.id)
        instance = await session.get(ObjectType, data.id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True, exclude={"id"}).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ObjectTypeSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity: GetSchema
    ) -> ObjectTypeSchema | None:
        log.info("Получаем запись ObjectType id=%s", entity.id)
        instance = await session.get(ObjectType, entity.id)
        if instance is None:
            return None
        return ObjectTypeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        log.info("Удаляем запись ObjectType id=%s", entity.id)
        instance = await session.get(ObjectType, entity.id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> list[ObjectTypeSchema]:
        log.info("Получаем все записи ObjectType")
        query = select(ObjectType)
        result = await session.execute(query)
        return [ObjectTypeSchema.model_validate(row) for row in result.scalars().all()]

    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[ObjectTypeSchema]:
        log.info(
            "Получаем записи ObjectType page=%s limit=%s",
            pagination.page,
            pagination.limit,
        )
        query = (
            select(ObjectType)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        result = await session.execute(query)
        return [ObjectTypeSchema.model_validate(row) for row in result.scalars().all()]

    async def get_children_by_parent(
        self, session: AsyncSession, parent_id: int
    ) -> list[ObjectTypeSchema]:
        """
        Получить список дочерних типов объектов по parent_id.

        Args:
            session: Асинхронная сессия SQLAlchemy
            parent_id: Идентификатор родительского типа объекта

        Returns:
            Список схем дочерних типов объектов
        """
        log.info("Получаем дочерние типы объектов для parent_id=%s", parent_id)
        query = select(ObjectType).where(ObjectType.parent_id == parent_id)
        result = await session.execute(query)
        return [ObjectTypeSchema.model_validate(row) for row in result.scalars().all()]
