import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.models.const_types import ObjectType
from backend_op.app.schemas.const_types_schemas import (
    ObjectTypeCreateSchema,
    ObjectTypeEditSchema,
    ObjectTypeSchema,
)

log = logging.getLogger(__name__)


class ObjectTypeHandler(
    BaseHandler[ObjectTypeCreateSchema, ObjectTypeEditSchema, ObjectTypeSchema]
):
    async def create(
        self, session: AsyncSession, data: ObjectTypeCreateSchema
    ) -> ObjectTypeSchema:
        log.info("Создаём запись ObjectType")
        instance = ObjectType(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ObjectTypeSchema.model_validate(instance)

    async def update(
        self,
        session: AsyncSession,
        entity_id: int,
        data: ObjectTypeEditSchema,
    ) -> ObjectTypeSchema | None:
        log.info("Обновляем запись ObjectType id=%s", entity_id)
        instance = await session.get(ObjectType, entity_id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ObjectTypeSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity_id: int
    ) -> ObjectTypeSchema | None:
        log.info("Получаем запись ObjectType id=%s", entity_id)
        instance = await session.get(ObjectType, entity_id)
        if instance is None:
            return None
        return ObjectTypeSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        log.info("Удаляем запись ObjectType id=%s", entity_id)
        instance = await session.get(ObjectType, entity_id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True
