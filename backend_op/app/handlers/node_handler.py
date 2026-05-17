import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.models.graph_models import Node
from backend_op.app.schemas.graph_models_schemas import (
    NodeCreateSchema,
    NodeSchema,
    NodeUpdateSchema,
)

log = logging.getLogger(__name__)


class NodeHandler(BaseHandler[NodeCreateSchema, NodeUpdateSchema, NodeSchema]):
    async def create(
        self, session: AsyncSession, data: NodeCreateSchema
    ) -> NodeSchema:
        log.info("Создаём запись Node")
        instance = Node(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return NodeSchema.model_validate(instance)

    async def update(
        self,
        session: AsyncSession,
        entity_id: int,
        data: NodeUpdateSchema,
    ) -> NodeSchema | None:
        log.info("Обновляем запись Node id=%s", entity_id)
        instance = await session.get(Node, entity_id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return NodeSchema.model_validate(instance)

    async def get(self, session: AsyncSession, entity_id: int) -> NodeSchema | None:
        log.info("Получаем запись Node id=%s", entity_id)
        instance = await session.get(Node, entity_id)
        if instance is None:
            return None
        return NodeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        log.info("Удаляем запись Node id=%s", entity_id)
        instance = await session.get(Node, entity_id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True
