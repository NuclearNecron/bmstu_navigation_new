import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_handler import BaseHandler
from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.models.const_types import ConnectionType
from app.schemas.const_types_schemas import (
    ConnectionTypeCreateSchema,
    ConnectionTypeSchema,
    ConnectionTypeUpdateSchema,
)

log = logging.getLogger(__name__)


class ConnectionTypeHandler(
    BaseHandler[
        ConnectionTypeCreateSchema,
        ConnectionTypeUpdateSchema,
        ConnectionTypeSchema,
    ]
):
    async def create(
        self, session: AsyncSession, data: ConnectionTypeCreateSchema
    ) -> ConnectionTypeSchema:
        log.info("Создаём запись ConnectionType")
        instance = ConnectionType(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ConnectionTypeSchema.model_validate(instance)

    async def update(
        self, session: AsyncSession, data: ConnectionTypeUpdateSchema
    ) -> ConnectionTypeSchema | None:
        log.info("Обновляем запись ConnectionType id=%s", data.id)
        instance = await session.get(ConnectionType, data.id)
        if instance is None:
            return None

        for field, value in data.model_dump(
            exclude_unset=True, exclude={"id"}
        ).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ConnectionTypeSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity: GetSchema
    ) -> ConnectionTypeSchema | None:
        log.info("Получаем запись ConnectionType id=%s", entity.id)
        instance = await session.get(ConnectionType, entity.id)
        if instance is None:
            return None
        return ConnectionTypeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        log.info("Удаляем запись ConnectionType id=%s", entity.id)
        instance = await session.get(ConnectionType, entity.id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> list[ConnectionTypeSchema]:
        log.info("Получаем все записи ConnectionType")
        query = select(ConnectionType)
        result = await session.execute(query)
        return [
            ConnectionTypeSchema.model_validate(row)
            for row in result.scalars().all()
        ]

    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[ConnectionTypeSchema]:
        log.info(
            "Получаем записи ConnectionType page=%s limit=%s",
            pagination.page,
            pagination.limit,
        )
        query = (
            select(ConnectionType)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        result = await session.execute(query)
        return [
            ConnectionTypeSchema.model_validate(row)
            for row in result.scalars().all()
        ]
