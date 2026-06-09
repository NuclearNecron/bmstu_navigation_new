from fastapi import Body, Path, Query
from pydantic import BaseModel

from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.schemas.graph_models_schemas import (
    NodeCreateSchema,
    NodeUpdateSchema,
)


class NodeGetAllParams(BaseModel):
    """Запрос списка всех узлов (без параметров)."""


class NodePaginatedParams(BaseModel):
    page: int
    limit: int

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class NodeGetParams(BaseModel):
    id: int

    def to_get_schema(self) -> GetSchema:
        return GetSchema(id=self.id)


class NodeDeleteParams(BaseModel):
    id: int

    def to_delete_schema(self) -> DeleteSchema:
        return DeleteSchema(id=self.id)


class NodeCreateParams(BaseModel):
    object_id: int
    type_id: int
    short_name: str
    full_name: str
    SVG: str | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    latitude: float | None = None
    longitude: float | None = None

    def to_create_schema(self) -> NodeCreateSchema:
        return NodeCreateSchema.model_validate(self.model_dump())


class NodeUpdateParams(BaseModel):
    id: int
    object_id: int | None = None
    type_id: int | None = None
    short_name: str | None = None
    full_name: str | None = None
    SVG: str | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    latitude: float | None = None
    longitude: float | None = None

    def to_edit_schema(self) -> NodeUpdateSchema:
        return NodeUpdateSchema.model_validate(self.model_dump())


def get_node_get_all_params() -> NodeGetAllParams:
    return NodeGetAllParams()


def get_node_paginated_params(
    page: int = Query(1, description="Номер страницы", ge=1),
    limit: int = Query(10, description="Количество записей на странице", ge=1, le=100),
) -> NodePaginatedParams:
    return NodePaginatedParams(page=page, limit=limit)


def get_node_get_params(
    id: int = Path(..., description="Идентификатор узла", ge=1),
) -> NodeGetParams:
    return NodeGetParams(id=id)


def get_node_delete_params(
    id: int = Path(..., description="Идентификатор узла", ge=1),
) -> NodeDeleteParams:
    return NodeDeleteParams(id=id)


def get_node_create_params(
    object_id: int = Body(..., description="Идентификатор объекта"),
    type_id: int = Body(..., description="Идентификатор типа узла"),
    short_name: str = Body(..., description="Краткое наименование", max_length=50),
    full_name: str = Body(..., description="Полное наименование", max_length=100),
    SVG: str | None = Body(None, description="SVG код узла"),
    x: float | None = Body(None, description="Координата X"),
    y: float | None = Body(None, description="Координата Y"),
    z: float | None = Body(None, description="Координата Z"),
    latitude: float | None = Body(None, description="Широта"),
    longitude: float | None = Body(None, description="Долгота"),
) -> NodeCreateParams:
    return NodeCreateParams(
        object_id=object_id,
        type_id=type_id,
        short_name=short_name,
        full_name=full_name,
        SVG=SVG,
        x=x,
        y=y,
        z=z,
        latitude=latitude,
        longitude=longitude,
    )


def get_node_update_params(
    id: int = Path(..., description="Идентификатор узла", ge=1),
    object_id: int | None = Body(None, description="Идентификатор объекта"),
    type_id: int | None = Body(None, description="Идентификатор типа узла"),
    short_name: str | None = Body(
        None, description="Краткое наименование", max_length=50
    ),
    full_name: str | None = Body(
        None, description="Полное наименование", max_length=100
    ),
    SVG: str | None = Body(None, description="SVG код узла"),
    x: float | None = Body(None, description="Координата X"),
    y: float | None = Body(None, description="Координата Y"),
    z: float | None = Body(None, description="Координата Z"),
    latitude: float | None = Body(None, description="Широта"),
    longitude: float | None = Body(None, description="Долгота"),
) -> NodeUpdateParams:
    return NodeUpdateParams(
        id=id,
        object_id=object_id,
        type_id=type_id,
        short_name=short_name,
        full_name=full_name,
        SVG=SVG,
        x=x,
        y=y,
        z=z,
        latitude=latitude,
        longitude=longitude,
    )
