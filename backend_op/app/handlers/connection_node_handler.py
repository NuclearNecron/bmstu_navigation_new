import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from backend_op.app.models.graph_models import ConnectionNode
from backend_op.app.schemas.graph_models_schemas import (
    ConnectionNodeCreateSchema,
    ConnectionNodeSchema,
    ConnectionNodeUpdateSchema,
)

log = logging.getLogger(__name__)


class ConnectionNodeHandler(
    BaseHandler[
        ConnectionNodeCreateSchema,
        ConnectionNodeUpdateSchema,
        ConnectionNodeSchema,
    ]
):
    async def create(
        self, session: AsyncSession, data: ConnectionNodeCreateSchema
    ) -> ConnectionNodeSchema:
        log.info("Создаём запись ConnectionNode")
        instance = ConnectionNode(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ConnectionNodeSchema.model_validate(instance)

    async def update(
        self, session: AsyncSession, data: ConnectionNodeUpdateSchema
    ) -> ConnectionNodeSchema | None:
        log.info("Обновляем запись ConnectionNode id=%s", data.id)
        instance = await session.get(ConnectionNode, data.id)
        if instance is None:
            return None

        for field, value in data.model_dump(
            exclude_unset=True, exclude={"id"}
        ).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ConnectionNodeSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity: GetSchema
    ) -> ConnectionNodeSchema | None:
        log.info("Получаем запись ConnectionNode id=%s", entity.id)
        instance = await session.get(ConnectionNode, entity.id)
        if instance is None:
            return None
        return ConnectionNodeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        log.info("Удаляем запись ConnectionNode id=%s", entity.id)
        instance = await session.get(ConnectionNode, entity.id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> list[ConnectionNodeSchema]:
        log.info("Получаем все записи ConnectionNode")
        query = select(ConnectionNode)
        result = await session.execute(query)
        return [
            ConnectionNodeSchema.model_validate(row)
            for row in result.scalars().all()
        ]

    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[ConnectionNodeSchema]:
        log.info(
            "Получаем записи ConnectionNode page=%s limit=%s",
            pagination.page,
            pagination.limit,
        )
        query = (
            select(ConnectionNode)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        result = await session.execute(query)
        return [
            ConnectionNodeSchema.model_validate(row)
            for row in result.scalars().all()
        ]
