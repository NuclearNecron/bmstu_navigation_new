import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from backend_op.app.models.const_types import ObjectKind
from backend_op.app.schemas.const_types_schemas import (
    ObjectKindCreateSchema,
    ObjectKindSchema,
    ObjectKindUpdateSchema,
)

log = logging.getLogger(__name__)


class ObjectKindHandler(
    BaseHandler[ObjectKindCreateSchema, ObjectKindUpdateSchema, ObjectKindSchema]
):
    async def create(
        self, session: AsyncSession, data: ObjectKindCreateSchema
    ) -> ObjectKindSchema:
        log.info("Создаём запись ObjectKind")
        instance = ObjectKind(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ObjectKindSchema.model_validate(instance)

    async def update(
        self, session: AsyncSession, data: ObjectKindUpdateSchema
    ) -> ObjectKindSchema | None:
        log.info("Обновляем запись ObjectKind id=%s", data.id)
        instance = await session.get(ObjectKind, data.id)
        if instance is None:
            return None

        for field, value in data.model_dump(
            exclude_unset=True, exclude={"id"}
        ).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ObjectKindSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity: GetSchema
    ) -> ObjectKindSchema | None:
        log.info("Получаем запись ObjectKind id=%s", entity.id)
        instance = await session.get(ObjectKind, entity.id)
        if instance is None:
            return None
        return ObjectKindSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        log.info("Удаляем запись ObjectKind id=%s", entity.id)
        instance = await session.get(ObjectKind, entity.id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True

    async def get_all(self, session: AsyncSession) -> list[ObjectKindSchema]:
        log.info("Получаем все записи ObjectKind")
        query = select(ObjectKind)
        result = await session.execute(query)
        return [
            ObjectKindSchema.model_validate(row)
            for row in result.scalars().all()
        ]

    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[ObjectKindSchema]:
        log.info(
            "Получаем записи ObjectKind page=%s limit=%s",
            pagination.page,
            pagination.limit,
        )
        query = (
            select(ObjectKind)
            .offset((pagination.page - 1) * pagination.limit)
            .limit(pagination.limit)
        )
        result = await session.execute(query)
        return [
            ObjectKindSchema.model_validate(row)
            for row in result.scalars().all()
        ]
