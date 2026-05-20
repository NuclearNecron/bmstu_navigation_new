import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_handler import BaseHandler
from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.models.object_models import ConnectionObject
from app.schemas.object_models_schemas import (
    ConnectionObjectCreateSchema,
    ConnectionObjectSchema,
    ConnectionObjectUpdateSchema,
)

log = logging.getLogger(__name__)


class ConnectionObjectHandler(
    BaseHandler[
        ConnectionObjectCreateSchema,
        ConnectionObjectUpdateSchema,
        ConnectionObjectSchema,
    ]
):
    async def create(
        self, session: AsyncSession, data: ConnectionObjectCreateSchema
    ) -> ConnectionObjectSchema:
        log.info("Создаём запись ConnectionObject")
        instance = ConnectionObject(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ConnectionObjectSchema.model_validate(instance)

    async def update(
        self, session: AsyncSession, data: ConnectionObjectUpdateSchema
    ) -> ConnectionObjectSchema | None:
        log.info("Обновляем запись ConnectionObject id=%s", data.id)
        instance = await session.get(ConnectionObject, data.id)
        if instance is None:
            return None

        for field, value in data.model_dump(
            exclude_unset=True, exclude={"id"}
        ).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ConnectionObjectSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity: GetSchema
    ) -> ConnectionObjectSchema | None:
        log.info("Получаем запись ConnectionObject id=%s", entity.id)
        instance = await session.get(ConnectionObject, entity.id)
        if instance is None:
            return None
        return ConnectionObjectSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        log.info("Удаляем запись ConnectionObject id=%s", entity.id)
        instance = await session.get(ConnectionObject, entity.id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> list[ConnectionObjectSchema]:
        log.info("Получаем все записи ConnectionObject")
        query = select(ConnectionObject)
        result = await session.execute(query)
        return [
            ConnectionObjectSchema.model_validate(row)
            for row in result.scalars().all()
        ]

    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[ConnectionObjectSchema]:
        log.info(
            "Получаем записи ConnectionObject page=%s limit=%s",
            pagination.page,
            pagination.limit,
        )
        query = (
            select(ConnectionObject)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        result = await session.execute(query)
        return [
            ConnectionObjectSchema.model_validate(row)
            for row in result.scalars().all()
        ]
