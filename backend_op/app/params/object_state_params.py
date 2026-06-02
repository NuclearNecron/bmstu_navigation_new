from fastapi import Body, Path, Query
from pydantic import BaseModel

from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.schemas.const_types_schemas import (
    ObjectStateCreateSchema,
    ObjectStateUpdateSchema,
)


class ObjectStateGetAllParams(BaseModel):
    """Запрос списка всех состояний объектов (без параметров)."""


class ObjectStatePaginatedParams(BaseModel):
    page: int
    limit: int

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class ObjectStateGetParams(BaseModel):
    id: int

    def to_get_schema(self) -> GetSchema:
        return GetSchema(id=self.id)


class ObjectStateDeleteParams(BaseModel):
    id: int

    def to_delete_schema(self) -> DeleteSchema:
        return DeleteSchema(id=self.id)


class ObjectStateCreateParams(BaseModel):
    short_name: str
    full_name: str
    description: str | None = None
    colour: str

    def to_create_schema(self) -> ObjectStateCreateSchema:
        return ObjectStateCreateSchema.model_validate(self.model_dump())


class ObjectStateUpdateParams(BaseModel):
    id: int
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None

    def to_edit_schema(self) -> ObjectStateUpdateSchema:
        return ObjectStateUpdateSchema.model_validate(self.model_dump())


def get_object_state_get_all_params() -> ObjectStateGetAllParams:
    return ObjectStateGetAllParams()


def get_object_state_paginated_params(
    page: int = Query(1, description="Номер страницы", ge=1),
    limit: int = Query(10, description="Количество записей на странице", ge=1, le=100),
) -> ObjectStatePaginatedParams:
    return ObjectStatePaginatedParams(page=page, limit=limit)


def get_object_state_get_params(
    id: int = Path(..., description="Идентификатор состояния объекта", ge=1),
) -> ObjectStateGetParams:
    return ObjectStateGetParams(id=id)


def get_object_state_delete_params(
    id: int = Path(..., description="Идентификатор состояния объекта", ge=1),
) -> ObjectStateDeleteParams:
    return ObjectStateDeleteParams(id=id)


def get_object_state_create_params(
    short_name: str = Body(..., description="Краткое наименование", max_length=50),
    full_name: str = Body(..., description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    colour: str = Body(..., description="Цвет", max_length=50),
) -> ObjectStateCreateParams:
    return ObjectStateCreateParams(
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
    )


def get_object_state_update_params(
    id: int = Path(..., description="Идентификатор состояния объекта", ge=1),
    short_name: str | None = Body(None, description="Краткое наименование", max_length=50),
    full_name: str | None = Body(None, description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    colour: str | None = Body(None, description="Цвет", max_length=50),
) -> ObjectStateUpdateParams:
    return ObjectStateUpdateParams(
        id=id,
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
    )