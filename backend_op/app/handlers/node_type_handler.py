import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.base.base_schemas import DeleteSchema, GetSchema, Pagination
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
        self, session: AsyncSession, data: NodeTypeUpdateSchema
    ) -> NodeTypeSchema | None:
        log.info("Обновляем запись NodeType id=%s", data.id)
        instance = await session.get(NodeType, data.id)
        if instance is None:
            return None

        for field, value in data.model_dump(
            exclude_unset=True, exclude={"id"}
        ).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return NodeTypeSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity: GetSchema
    ) -> NodeTypeSchema | None:
        log.info("Получаем запись NodeType id=%s", entity.id)
        instance = await session.get(NodeType, entity.id)
        if instance is None:
            return None
        return NodeTypeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        log.info("Удаляем запись NodeType id=%s", entity.id)
        instance = await session.get(NodeType, entity.id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> list[NodeTypeSchema]:
        log.info("Получаем все записи NodeType")
        query = select(NodeType)
        result = await session.execute(query)
        return [
            NodeTypeSchema.model_validate(row)
            for row in result.scalars().all()
        ]

    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[NodeTypeSchema]:
        log.info(
            "Получаем записи NodeType page=%s limit=%s",
            pagination.page,
            pagination.limit,
        )
        query = (
            select(NodeType)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        result = await session.execute(query)
        return [
            NodeTypeSchema.model_validate(row)
            for row in result.scalars().all()
        ]
