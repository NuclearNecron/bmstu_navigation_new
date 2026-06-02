from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.base_schemas import DeleteSchema, GetSchema, Pagination

CreateT = TypeVar("CreateT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)
ReadT = TypeVar("ReadT", bound=BaseModel)


class BaseHandler(ABC, Generic[CreateT, UpdateT, ReadT]):
    """Абстрактный CRUD-контракт. Схемы передаются в аргументах методов."""

    @abstractmethod
    async def create(self, session: AsyncSession, data: CreateT) -> ReadT:
        """Создать запись."""

    @abstractmethod
    async def update(self, session: AsyncSession, data: UpdateT) -> ReadT | None:
        """Обновить запись. Идентификатор передаётся в data."""

    @abstractmethod
    async def get(self, session: AsyncSession, entity: GetSchema) -> ReadT | None:
        """Получить одну запись по идентификатору."""

    @abstractmethod
    async def delete(self, session: AsyncSession, entity: DeleteSchema) -> bool:
        """Удалить запись по идентификатору."""

    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[ReadT]:
        """Получить все записи."""

    @abstractmethod
    async def get_paginated(
        self, session: AsyncSession, pagination: Pagination
    ) -> list[ReadT]:
        """Получить записи с пагинацией."""
