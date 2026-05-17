import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.models.const_types import ConnectionType
from backend_op.app.schemas.const_types_schemas import (
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
        self,
        session: AsyncSession,
        entity_id: int,
        data: ConnectionTypeUpdateSchema,
    ) -> ConnectionTypeSchema | None:
        log.info("Обновляем запись ConnectionType id=%s", entity_id)
        instance = await session.get(ConnectionType, entity_id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ConnectionTypeSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity_id: int
    ) -> ConnectionTypeSchema | None:
        log.info("Получаем запись ConnectionType id=%s", entity_id)
        instance = await session.get(ConnectionType, entity_id)
        if instance is None:
            return None
        return ConnectionTypeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        log.info("Удаляем запись ConnectionType id=%s", entity_id)
        instance = await session.get(ConnectionType, entity_id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True
