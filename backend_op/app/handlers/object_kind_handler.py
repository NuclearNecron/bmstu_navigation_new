import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend_op.app.base.base_handler import BaseHandler
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
        self,
        session: AsyncSession,
        entity_id: int,
        data: ObjectKindUpdateSchema,
    ) -> ObjectKindSchema | None:
        log.info("Обновляем запись ObjectKind id=%s", entity_id)
        instance = await session.get(ObjectKind, entity_id)
        if instance is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)

        await session.commit()
        await session.refresh(instance)
        return ObjectKindSchema.model_validate(instance)

    async def get(
        self, session: AsyncSession, entity_id: int
    ) -> ObjectKindSchema | None:
        log.info("Получаем запись ObjectKind id=%s", entity_id)
        instance = await session.get(ObjectKind, entity_id)
        if instance is None:
            return None
        return ObjectKindSchema.model_validate(instance)

    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        log.info("Удаляем запись ObjectKind id=%s", entity_id)
        instance = await session.get(ObjectKind, entity_id)
        if instance is None:
            return False

        await session.delete(instance)
        await session.commit()
        return True
