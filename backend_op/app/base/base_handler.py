from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

CreateT = TypeVar("CreateT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)
ReadT = TypeVar("ReadT", bound=BaseModel)


class BaseHandler(ABC, Generic[CreateT, UpdateT, ReadT]):
    """Абстрактный CRUD-контракт. Схемы передаются в аргументах методов."""

    @abstractmethod
    async def create(self, session: AsyncSession, data: CreateT) -> ReadT:
        """Создать запись."""

    @abstractmethod
    async def update(
        self, session: AsyncSession, entity_id: int, data: UpdateT
    ) -> ReadT | None:
        """Обновить запись по идентификатору."""

    @abstractmethod
    async def get(self, session: AsyncSession, entity_id: int) -> ReadT | None:
        """Получить одну запись по идентификатору."""

    @abstractmethod
    async def delete(self, session: AsyncSession, entity_id: int) -> bool:
        """Удалить запись по идентификатору."""
