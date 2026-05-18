import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from backend_op.app.models.object_models import Object
from backend_op.app.schemas.object_models_schemas import (
    ObjectCreateSchema,
    ObjectSchema,
    ObjectUpdateSchema,
)

log = logging.getLogger(__name__)


class ObjectHandler(
    BaseHandler[ObjectCreateSchema, ObjectUpdateSchema, ObjectSchema]
):
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

        for field, value in data.model_dump(
            exclude_unset=True, exclude={"id"}
        ).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ObjectSchema.model_validate(instance)

    async def get(self, session: AsyncSession, entity: GetSchema) -> ObjectSchema | None:
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
        return [
            ObjectSchema.model_validate(row)
            for row in result.scalars().all()
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
        return [
            ObjectSchema.model_validate(row)
            for row in result.scalars().all()
        ]
