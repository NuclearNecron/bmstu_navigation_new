import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.models.object_models import Object
from backend_op.app.schemas.object_models_schemas import (
    ObjectCreateSchema,
    ObjectSchema,
    ObjectUpdateSchema,
)

log = logging.getLogger(__name__)


class ObjectHandler(
    BaseHandler[ObjectCreateSchema, ObjectUpdateSchema, ObjectSchema]
):
    async def create(
        self, session: AsyncSession, data: ObjectCreateSchema
    ) -> ObjectSchema:
        log.info("Создаём запись Object")
        instance = Object(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ObjectSchema.model_validate(instance)

    async def update(
        self,
        session: AsyncSession,
        entity_id: int,
        data: ObjectUpdateSchema,
    ) -> ObjectSchema | None:
        log.info("Обновляем запись Object id=%s", entity_id)
        instance = await session.get(Object, entity_id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ObjectSchema.model_validate(instance)

    async def get(self, session: AsyncSession, entity_id: int) -> ObjectSchema | None:
        log.info("Получаем запись Object id=%s", entity_id)
        instance = await session.get(Object, entity_id)
        if instance is None:
            return None
        return ObjectSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        log.info("Удаляем запись Object id=%s", entity_id)
        instance = await session.get(Object, entity_id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True
