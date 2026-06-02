from fastapi import Body, Path, Query
from pydantic import BaseModel

from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.schemas.const_types_schemas import (
    ObjectTypeCreateSchema,
    ObjectTypeEditSchema,
)


class ObjectTypeGetAllParams(BaseModel):
    """Запрос списка всех типов объектов (без параметров)."""


class ObjectTypePaginatedParams(BaseModel):
    page: int
    limit: int

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class ObjectTypeGetParams(BaseModel):
    id: int

    def to_get_schema(self) -> GetSchema:
        return GetSchema(id=self.id)


class ObjectTypeDeleteParams(BaseModel):
    id: int

    def to_delete_schema(self) -> DeleteSchema:
        return DeleteSchema(id=self.id)


class ObjectTypeCreateParams(BaseModel):
    parent_id: int | None = None
    short_name: str
    full_name: str
    description: str | None = None
    colour: str

    def to_create_schema(self) -> ObjectTypeCreateSchema:
        return ObjectTypeCreateSchema.model_validate(self.model_dump())


class ObjectTypeUpdateParams(BaseModel):
    id: int
    parent_id: int | None = None
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None

    def to_edit_schema(self) -> ObjectTypeEditSchema:
        return ObjectTypeEditSchema.model_validate(self.model_dump())


class ObjectTypeGetChildrenParams(BaseModel):
    parent_id: int

    def to_get_children_schema(self) -> GetSchema:
        return GetSchema(id=self.parent_id)


def get_object_type_get_all_params() -> ObjectTypeGetAllParams:
    return ObjectTypeGetAllParams()


def get_object_type_paginated_params(
    page: int = Query(1, description="Номер страницы", ge=1),
    limit: int = Query(10, description="Количество записей на странице", ge=1, le=100),
) -> ObjectTypePaginatedParams:
    return ObjectTypePaginatedParams(page=page, limit=limit)


def get_object_type_get_params(
    id: int = Path(..., description="Идентификатор типа объекта", ge=1),
) -> ObjectTypeGetParams:
    return ObjectTypeGetParams(id=id)


def get_object_type_delete_params(
    id: int = Path(..., description="Идентификатор типа объекта", ge=1),
) -> ObjectTypeDeleteParams:
    return ObjectTypeDeleteParams(id=id)


def get_object_type_create_params(
    parent_id: int | None = Body(
        None, description="Идентификатор родительского типа объекта"
    ),
    short_name: str = Body(..., description="Краткое наименование", max_length=50),
    full_name: str = Body(..., description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    colour: str = Body(..., description="Цвет", max_length=50),
) -> ObjectTypeCreateParams:
    return ObjectTypeCreateParams(
        parent_id=parent_id,
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
    )


def get_object_type_update_params(
    id: int = Path(..., description="Идентификатор типа объекта", ge=1),
    parent_id: int | None = Body(
        None, description="Идентификатор родительского типа объекта"
    ),
    short_name: str | None = Body(
        None, description="Краткое наименование", max_length=50
    ),
    full_name: str | None = Body(
        None, description="Полное наименование", max_length=100
    ),
    description: str | None = Body(None, description="Описание"),
    colour: str | None = Body(None, description="Цвет", max_length=50),
) -> ObjectTypeUpdateParams:
    return ObjectTypeUpdateParams(
        id=id,
        parent_id=parent_id,
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
    )


def get_object_type_get_children_params(
    parent_id: int = Path(
        ..., description="Идентификатор родительского типа объекта", ge=1
    ),
) -> ObjectTypeGetChildrenParams:
    return ObjectTypeGetChildrenParams(parent_id=parent_id)
