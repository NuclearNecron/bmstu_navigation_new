from fastapi import Body, Path, Query
from pydantic import BaseModel

from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.schemas.const_types_schemas import (
    ConnectionTypeCreateSchema,
    ConnectionTypeUpdateSchema,
)


class ConnectionTypeGetAllParams(BaseModel):
    """Запрос списка всех типов соединений (без параметров)."""


class ConnectionTypePaginatedParams(BaseModel):
    page: int
    limit: int

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class ConnectionTypeGetParams(BaseModel):
    id: int

    def to_get_schema(self) -> GetSchema:
        return GetSchema(id=self.id)


class ConnectionTypeDeleteParams(BaseModel):
    id: int

    def to_delete_schema(self) -> DeleteSchema:
        return DeleteSchema(id=self.id)


class ConnectionTypeCreateParams(BaseModel):
    short_name: str
    full_name: str
    description: str | None = None
    colour: str
    style: str | None = None

    def to_create_schema(self) -> ConnectionTypeCreateSchema:
        return ConnectionTypeCreateSchema.model_validate(self.model_dump())


class ConnectionTypeUpdateParams(BaseModel):
    id: int
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None
    style: str | None = None

    def to_edit_schema(self) -> ConnectionTypeUpdateSchema:
        return ConnectionTypeUpdateSchema.model_validate(self.model_dump())


def get_connection_type_get_all_params() -> ConnectionTypeGetAllParams:
    return ConnectionTypeGetAllParams()


def get_connection_type_paginated_params(
    page: int = Query(1, description="Номер страницы", ge=1),
    limit: int = Query(10, description="Количество записей на странице", ge=1, le=100),
) -> ConnectionTypePaginatedParams:
    return ConnectionTypePaginatedParams(page=page, limit=limit)


def get_connection_type_get_params(
    id: int = Path(..., description="Идентификатор типа соединения", ge=1),
) -> ConnectionTypeGetParams:
    return ConnectionTypeGetParams(id=id)


def get_connection_type_delete_params(
    id: int = Path(..., description="Идентификатор типа соединения", ge=1),
) -> ConnectionTypeDeleteParams:
    return ConnectionTypeDeleteParams(id=id)


def get_connection_type_create_params(
    short_name: str = Body(..., description="Краткое наименование", max_length=50),
    full_name: str = Body(..., description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    colour: str = Body(..., description="Цвет", max_length=50),
    style: str | None = Body(None, description="Стиль соединения"),
) -> ConnectionTypeCreateParams:
    return ConnectionTypeCreateParams(
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
        style=style,
    )


def get_connection_type_update_params(
    id: int = Path(..., description="Идентификатор типа соединения", ge=1),
    short_name: str | None = Body(None, description="Краткое наименование", max_length=50),
    full_name: str | None = Body(None, description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    colour: str | None = Body(None, description="Цвет", max_length=50),
    style: str | None = Body(None, description="Стиль соединения"),
) -> ConnectionTypeUpdateParams:
    return ConnectionTypeUpdateParams(
        id=id,
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
        style=style,
    )