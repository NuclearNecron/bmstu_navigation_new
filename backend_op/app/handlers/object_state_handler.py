import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_handler import BaseHandler
from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.models.const_types import ObjectState
from app.schemas.const_types_schemas import (
    ObjectStateCreateSchema,
    ObjectStateSchema,
    ObjectStateUpdateSchema,
)

log = logging.getLogger(__name__)


class ObjectStateHandler(
    BaseHandler[ObjectStateCreateSchema, ObjectStateUpdateSchema, ObjectStateSchema]
):
    async def create(
        self, session: AsyncSession, data: ObjectStateCreateSchema
    ) -> ObjectStateSchema:
        log.info("Создаём запись ObjectState")
        instance = ObjectState(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ObjectStateSchema.model_validate(instance)

    async def update(
        self, session: AsyncSession, data: ObjectStateUpdateSchema
    ) -> ObjectStateSchema | None:
        log.info("Обновляем запись ObjectState id=%s", data.id)
        instance = await session.get(ObjectState, data.id)
        if instance is None:
            return None

        for field, value in data.model_dump(
            exclude_unset=True, exclude={"id"}
        ).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ObjectStateSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity: GetSchema
    ) -> ObjectStateSchema | None:
        log.info("Получаем запись ObjectState id=%s", entity.id)
        instance = await session.get(ObjectState, entity.id)
        if instance is None:
            return None
        return ObjectStateSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        log.info("Удаляем запись ObjectState id=%s", entity.id)
        instance = await session.get(ObjectState, entity.id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> list[ObjectStateSchema]:
        log.info("Получаем все записи ObjectState")
        query = select(ObjectState)
        result = await session.execute(query)
        return [
            ObjectStateSchema.model_validate(row)
            for row in result.scalars().all()
        ]

    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[ObjectStateSchema]:
        log.info(
            "Получаем записи ObjectState page=%s limit=%s",
            pagination.page,
            pagination.limit,
        )
        query = (
            select(ObjectState)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        result = await session.execute(query)
        return [
            ObjectStateSchema.model_validate(row)
            for row in result.scalars().all()
        ]
