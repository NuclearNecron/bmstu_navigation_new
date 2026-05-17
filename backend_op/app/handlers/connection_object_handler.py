import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.models.object_models import ConnectionObject
from backend_op.app.schemas.object_models_schemas import (
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
        self,
        session: AsyncSession,
        entity_id: int,
        data: ConnectionObjectUpdateSchema,
    ) -> ConnectionObjectSchema | None:
        log.info("Обновляем запись ConnectionObject id=%s", entity_id)
        instance = await session.get(ConnectionObject, entity_id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ConnectionObjectSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity_id: int
    ) -> ConnectionObjectSchema | None:
        log.info("Получаем запись ConnectionObject id=%s", entity_id)
        instance = await session.get(ConnectionObject, entity_id)
        if instance is None:
            return None
        return ConnectionObjectSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        log.info("Удаляем запись ConnectionObject id=%s", entity_id)
        instance = await session.get(ConnectionObject, entity_id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True
