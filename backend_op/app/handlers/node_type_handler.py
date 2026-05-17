import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.models.graph_models import NodeType
from backend_op.app.schemas.graph_models_schemas import (
    NodeTypeCreateSchema,
    NodeTypeSchema,
    NodeTypeUpdateSchema,
)

log = logging.getLogger(__name__)


class NodeTypeHandler(
    BaseHandler[NodeTypeCreateSchema, NodeTypeUpdateSchema, NodeTypeSchema]
):
    async def create(
        self, session: AsyncSession, data: NodeTypeCreateSchema
    ) -> NodeTypeSchema:
        log.info("Создаём запись NodeType")
        instance = NodeType(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return NodeTypeSchema.model_validate(instance)

    async def update(
        self,
        session: AsyncSession,
        entity_id: int,
        data: NodeTypeUpdateSchema,
    ) -> NodeTypeSchema | None:
        log.info("Обновляем запись NodeType id=%s", entity_id)
        instance = await session.get(NodeType, entity_id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return NodeTypeSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity_id: int
    ) -> NodeTypeSchema | None:
        log.info("Получаем запись NodeType id=%s", entity_id)
        instance = await session.get(NodeType, entity_id)
        if instance is None:
            return None
        return NodeTypeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        log.info("Удаляем запись NodeType id=%s", entity_id)
        instance = await session.get(NodeType, entity_id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True
