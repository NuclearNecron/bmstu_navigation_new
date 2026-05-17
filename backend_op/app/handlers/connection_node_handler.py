import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
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
        self,
        session: AsyncSession,
        entity_id: int,
        data: ConnectionNodeUpdateSchema,
    ) -> ConnectionNodeSchema | None:
        log.info("Обновляем запись ConnectionNode id=%s", entity_id)
        instance = await session.get(ConnectionNode, entity_id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ConnectionNodeSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity_id: int
    ) -> ConnectionNodeSchema | None:
        log.info("Получаем запись ConnectionNode id=%s", entity_id)
        instance = await session.get(ConnectionNode, entity_id)
        if instance is None:
            return None
        return ConnectionNodeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        log.info("Удаляем запись ConnectionNode id=%s", entity_id)
        instance = await session.get(ConnectionNode, entity_id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True
