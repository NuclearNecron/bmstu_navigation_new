from fastapi import Body, Path, Query
from pydantic import BaseModel

from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.schemas.const_types_schemas import (
    ObjectKindCreateSchema,
    ObjectKindUpdateSchema,
)


class ObjectKindGetAllParams(BaseModel):
    """Запрос списка всех видов объектов (без параметров)."""


class ObjectKindPaginatedParams(BaseModel):
    page: int
    limit: int

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class ObjectKindGetParams(BaseModel):
    id: int

    def to_get_schema(self) -> GetSchema:
        return GetSchema(id=self.id)


class ObjectKindDeleteParams(BaseModel):
    id: int

    def to_delete_schema(self) -> DeleteSchema:
        return DeleteSchema(id=self.id)


class ObjectKindCreateParams(BaseModel):
    parent_id: int | None = None
    type_id: int
    number: int
    short_name: str
    full_name: str
    description: str | None = None
    colour: str

    def to_create_schema(self) -> ObjectKindCreateSchema:
        return ObjectKindCreateSchema.model_validate(self.model_dump())


class ObjectKindUpdateParams(BaseModel):
    id: int
    parent_id: int | None = None
    type_id: int | None = None
    number: int | None = None
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None

    def to_edit_schema(self) -> ObjectKindUpdateSchema:
        return ObjectKindUpdateSchema.model_validate(self.model_dump())


class ObjectKindGetChildrenParams(BaseModel):
    parent_id: int

    def to_get_children_schema(self) -> GetSchema:
        return GetSchema(id=self.parent_id)


def get_object_kind_get_all_params() -> ObjectKindGetAllParams:
    return ObjectKindGetAllParams()


def get_object_kind_paginated_params(
    page: int = Query(1, description="Номер страницы", ge=1),
    limit: int = Query(10, description="Количество записей на странице", ge=1, le=100),
) -> ObjectKindPaginatedParams:
    return ObjectKindPaginatedParams(page=page, limit=limit)


def get_object_kind_get_params(
    id: int = Path(..., description="Идентификатор вида объекта", ge=1),
) -> ObjectKindGetParams:
    return ObjectKindGetParams(id=id)


def get_object_kind_delete_params(
    id: int = Path(..., description="Идентификатор вида объекта", ge=1),
) -> ObjectKindDeleteParams:
    return ObjectKindDeleteParams(id=id)


def get_object_kind_create_params(
    parent_id: int | None = Body(None, description="Идентификатор родительского вида объекта"),
    type_id: int = Body(..., description="Идентификатор типа объекта"),
    number: int = Body(..., description="Порядковый номер"),
    short_name: str = Body(..., description="Краткое наименование", max_length=50),
    full_name: str = Body(..., description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    colour: str = Body(..., description="Цвет", max_length=50),
) -> ObjectKindCreateParams:
    return ObjectKindCreateParams(
        parent_id=parent_id,
        type_id=type_id,
        number=number,
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
    )


def get_object_kind_update_params(
    id: int = Path(..., description="Идентификатор вида объекта", ge=1),
    parent_id: int | None = Body(None, description="Идентификатор родительского вида объекта"),
    type_id: int | None = Body(None, description="Идентификатор типа объекта"),
    number: int | None = Body(None, description="Порядковый номер"),
    short_name: str | None = Body(None, description="Краткое наименование", max_length=50),
    full_name: str | None = Body(None, description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    colour: str | None = Body(None, description="Цвет", max_length=50),
) -> ObjectKindUpdateParams:
    return ObjectKindUpdateParams(
        id=id,
        parent_id=parent_id,
        type_id=type_id,
        number=number,
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
    )


def get_object_kind_get_children_params(
    parent_id: int = Path(..., description="Идентификатор родительского вида объекта", ge=1),
) -> ObjectKindGetChildrenParams:
    return ObjectKindGetChildrenParams(parent_id=parent_id)