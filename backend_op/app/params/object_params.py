from fastapi import Body, Path, Query
from pydantic import BaseModel

from backend_op.app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from backend_op.app.schemas.object_models_schemas import (
    ObjectCreateSchema,
    ObjectUpdateSchema,
)


class ObjectGetAllParams(BaseModel):
    """Запрос списка всех объектов (без параметров)."""


class ObjectPaginatedParams(BaseModel):
    page: int
    limit: int

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class ObjectGetParams(BaseModel):
    id: int

    def to_get_schema(self) -> GetSchema:
        return GetSchema(id=self.id)


class ObjectDeleteParams(BaseModel):
    id: int

    def to_delete_schema(self) -> DeleteSchema:
        return DeleteSchema(id=self.id)


class ObjectCreateParams(BaseModel):
    parent_id: int | None = None
    kind_id: int
    state_id: int
    number: int
    short_name: str
    full_name: str
    description: str | None = None
    address: str | None = None
    plan_link: str | None = None
    blueprint_link: str | None = None
    scale: str | None = None
    height: float | None = None
    SVG: str | None = None

    def to_create_schema(self) -> ObjectCreateSchema:
        return ObjectCreateSchema.model_validate(self.model_dump())


class ObjectUpdateParams(BaseModel):
    id: int
    parent_id: int | None = None
    kind_id: int | None = None
    state_id: int | None = None
    number: int | None = None
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    address: str | None = None
    plan_link: str | None = None
    blueprint_link: str | None = None
    scale: str | None = None
    height: float | None = None
    SVG: str | None = None

    def to_edit_schema(self) -> ObjectUpdateSchema:
        return ObjectUpdateSchema.model_validate(self.model_dump())


def get_object_get_all_params() -> ObjectGetAllParams:
    return ObjectGetAllParams()


def get_object_paginated_params(
    page: int = Query(1, description="Номер страницы", ge=1),
    limit: int = Query(10, description="Количество записей на странице", ge=1, le=100),
) -> ObjectPaginatedParams:
    return ObjectPaginatedParams(page=page, limit=limit)


def get_object_get_params(
    id: int = Path(..., description="Идентификатор объекта", ge=1),
) -> ObjectGetParams:
    return ObjectGetParams(id=id)


def get_object_delete_params(
    id: int = Path(..., description="Идентификатор объекта", ge=1),
) -> ObjectDeleteParams:
    return ObjectDeleteParams(id=id)


def get_object_create_params(
    parent_id: int | None = Body(None, description="Идентификатор родительского объекта"),
    kind_id: int = Body(..., description="Идентификатор вида объекта"),
    state_id: int = Body(..., description="Идентификатор состояния объекта"),
    number: int = Body(..., description="Порядковый номер"),
    short_name: str = Body(..., description="Краткое наименование", max_length=50),
    full_name: str = Body(..., description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    address: str | None = Body(None, description="Адрес объекта"),
    plan_link: str | None = Body(None, description="Ссылка на план"),
    blueprint_link: str | None = Body(None, description="Ссылка на чертеж"),
    scale: str | None = Body(None, description="Масштаб"),
    height: float | None = Body(None, description="Высота"),
    SVG: str | None = Body(None, description="SVG код объекта"),
) -> ObjectCreateParams:
    return ObjectCreateParams(
        parent_id=parent_id,
        kind_id=kind_id,
        state_id=state_id,
        number=number,
        short_name=short_name,
        full_name=full_name,
        description=description,
        address=address,
        plan_link=plan_link,
        blueprint_link=blueprint_link,
        scale=scale,
        height=height,
        SVG=SVG,
    )


def get_object_update_params(
    id: int = Path(..., description="Идентификатор объекта", ge=1),
    parent_id: int | None = Body(None, description="Идентификатор родительского объекта"),
    kind_id: int | None = Body(None, description="Идентификатор вида объекта"),
    state_id: int | None = Body(None, description="Идентификатор состояния объекта"),
    number: int | None = Body(None, description="Порядковый номер"),
    short_name: str | None = Body(None, description="Краткое наименование", max_length=50),
    full_name: str | None = Body(None, description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    address: str | None = Body(None, description="Адрес объекта"),
    plan_link: str | None = Body(None, description="Ссылка на план"),
    blueprint_link: str | None = Body(None, description="Ссылка на чертеж"),
    scale: str | None = Body(None, description="Масштаб"),
    height: float | None = Body(None, description="Высота"),
    SVG: str | None = Body(None, description="SVG код объекта"),
) -> ObjectUpdateParams:
    return ObjectUpdateParams(
        id=id,
        parent_id=parent_id,
        kind_id=kind_id,
        state_id=state_id,
        number=number,
        short_name=short_name,
        full_name=full_name,
        description=description,
        address=address,
        plan_link=plan_link,
        blueprint_link=blueprint_link,
        scale=scale,
        height=height,
        SVG=SVG,
    )