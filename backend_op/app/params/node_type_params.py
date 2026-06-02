from fastapi import Body, Path, Query
from pydantic import BaseModel

from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.schemas.graph_models_schemas import (
    NodeTypeCreateSchema,
    NodeTypeUpdateSchema,
)


class NodeTypeGetAllParams(BaseModel):
    """Запрос списка всех типов узлов (без параметров)."""


class NodeTypePaginatedParams(BaseModel):
    page: int
    limit: int

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class NodeTypeGetParams(BaseModel):
    id: int

    def to_get_schema(self) -> GetSchema:
        return GetSchema(id=self.id)


class NodeTypeDeleteParams(BaseModel):
    id: int

    def to_delete_schema(self) -> DeleteSchema:
        return DeleteSchema(id=self.id)


class NodeTypeCreateParams(BaseModel):
    short_name: str
    full_name: str
    description: str | None = None
    colour: str
    size: float

    def to_create_schema(self) -> NodeTypeCreateSchema:
        return NodeTypeCreateSchema.model_validate(self.model_dump())


class NodeTypeUpdateParams(BaseModel):
    id: int
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None
    size: float | None = None

    def to_edit_schema(self) -> NodeTypeUpdateSchema:
        return NodeTypeUpdateSchema.model_validate(self.model_dump())


def get_node_type_get_all_params() -> NodeTypeGetAllParams:
    return NodeTypeGetAllParams()


def get_node_type_paginated_params(
    page: int = Query(1, description="Номер страницы", ge=1),
    limit: int = Query(10, description="Количество записей на странице", ge=1, le=100),
) -> NodeTypePaginatedParams:
    return NodeTypePaginatedParams(page=page, limit=limit)


def get_node_type_get_params(
    id: int = Path(..., description="Идентификатор типа узла", ge=1),
) -> NodeTypeGetParams:
    return NodeTypeGetParams(id=id)


def get_node_type_delete_params(
    id: int = Path(..., description="Идентификатор типа узла", ge=1),
) -> NodeTypeDeleteParams:
    return NodeTypeDeleteParams(id=id)


def get_node_type_create_params(
    short_name: str = Body(..., description="Краткое наименование", max_length=50),
    full_name: str = Body(..., description="Полное наименование", max_length=100),
    description: str | None = Body(None, description="Описание"),
    colour: str = Body(..., description="Цвет", max_length=50),
    size: float = Body(..., description="Размер узла"),
) -> NodeTypeCreateParams:
    return NodeTypeCreateParams(
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
        size=size,
    )


def get_node_type_update_params(
    id: int = Path(..., description="Идентификатор типа узла", ge=1),
    short_name: str | None = Body(
        None, description="Краткое наименование", max_length=50
    ),
    full_name: str | None = Body(
        None, description="Полное наименование", max_length=100
    ),
    description: str | None = Body(None, description="Описание"),
    colour: str | None = Body(None, description="Цвет", max_length=50),
    size: float | None = Body(None, description="Размер узла"),
) -> NodeTypeUpdateParams:
    return NodeTypeUpdateParams(
        id=id,
        short_name=short_name,
        full_name=full_name,
        description=description,
        colour=colour,
        size=size,
    )
