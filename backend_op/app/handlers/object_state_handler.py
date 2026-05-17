import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
from backend_op.app.models.const_types import ObjectState
from backend_op.app.schemas.const_types_schemas import (
    ObjectStateCreateSchema,
    ObjectStateSchema,
    ObjectStateUpdateSchema,
)

log = logging.getLogger(__name__)


class ObjectStateHandler(
    BaseHandler[ObjectStateCreateSchema, ObjectStateUpdateSchema, ObjectStateSchema]
):
    async def create(
        self, session: AsyncSession, data: ObjectStateCreateSchema
    ) -> ObjectStateSchema:
        log.info("Создаём запись ObjectState")
        instance = ObjectState(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return ObjectStateSchema.model_validate(instance)

    async def update(
        self,
        session: AsyncSession,
        entity_id: int,
        data: ObjectStateUpdateSchema,
    ) -> ObjectStateSchema | None:
        log.info("Обновляем запись ObjectState id=%s", entity_id)
        instance = await session.get(ObjectState, entity_id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ObjectStateSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity_id: int
    ) -> ObjectStateSchema | None:
        log.info("Получаем запись ObjectState id=%s", entity_id)
        instance = await session.get(ObjectState, entity_id)
        if instance is None:
            return None
        return ObjectStateSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        log.info("Удаляем запись ObjectState id=%s", entity_id)
        instance = await session.get(ObjectState, entity_id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True
