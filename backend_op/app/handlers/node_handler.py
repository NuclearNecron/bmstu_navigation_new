import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_handler import BaseHandler
from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.models.graph_models import Node
from app.schemas.graph_models_schemas import (
    NodeCreateSchema,
    NodeUpdateSchema,
    NodeSchema,
    NodeMapperSchema,
)

log = logging.getLogger(__name__)


class NodeHandler(BaseHandler[NodeCreateSchema, NodeUpdateSchema, NodeSchema]):
    async def create(self, session: AsyncSession, data: NodeCreateSchema) -> NodeSchema:
        log.info("Создаём запись Node")
        instance = Node(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return NodeSchema.model_validate(instance)

    async def update(
        self, session: AsyncSession, data: NodeUpdateSchema
    ) -> NodeSchema | None:
        log.info("Обновляем запись Node id=%s", data.id)
        instance = await session.get(Node, data.id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True, exclude={"id"}).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return NodeSchema.model_validate(instance)

    async def get(self, session: AsyncSession, entity: GetSchema) -> NodeSchema | None:
        log.info("Получаем запись Node id=%s", entity.id)
        instance = await session.get(Node, entity.id)
        if instance is None:
            return None
        return NodeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        log.info("Удаляем запись Node id=%s", entity.id)
        instance = await session.get(Node, entity.id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> list[NodeSchema]:
        log.info("Получаем все записи Node")
        query = select(Node)
        result = await session.execute(query)
        return [NodeSchema.model_validate(row) for row in result.scalars().all()]

    async def get_all_mapped(self, session: AsyncSession) -> list[NodeMapperSchema]:
        query = select(
            Node.id,
            Node.object_id,
            Node.latitude,
            Node.longitude,
            Node.short_name,
            Node.x,
            Node.y,
            Node.z,
        )
        result = await session.execute(query)
        return [NodeMapperSchema.model_validate(row) for row in result.mappings().all()]

    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[NodeSchema]:
        log.info(
            "Получаем записи Node page=%s limit=%s",
            pagination.page,
            pagination.limit,
        )
        query = (
            select(Node)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        result = await session.execute(query)
        return [NodeSchema.model_validate(row) for row in result.scalars().all()]
