from fastapi import Body, Path, Query
from pydantic import BaseModel

from backend_op.app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from backend_op.app.schemas.graph_models_schemas import (
    ConnectionNodeCreateSchema,
    ConnectionNodeUpdateSchema,
)


class ConnectionNodeGetAllParams(BaseModel):
    """Запрос списка всех соединений узлов (без параметров)."""


class ConnectionNodePaginatedParams(BaseModel):
    page: int
    limit: int

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class ConnectionNodeGetParams(BaseModel):
    id: int

    def to_get_schema(self) -> GetSchema:
        return GetSchema(id=self.id)


class ConnectionNodeDeleteParams(BaseModel):
    id: int

    def to_delete_schema(self) -> DeleteSchema:
        return DeleteSchema(id=self.id)



class ConnectionNodeCreateParams(BaseModel):
    node_id1: int
    node_id2: int
    connection_type_id: int | None = None
    distance: float

    def to_create_schema(self) -> ConnectionNodeCreateSchema:
        return ConnectionNodeCreateSchema.model_validate(self.model_dump())


class ConnectionNodeUpdateParams(BaseModel):
    id: int
    node_id1: int | None = None
    node_id2: int | None = None
    connection_type_id: int | None = None
    distance: float | None = None

    def to_edit_schema(self) -> ConnectionNodeUpdateSchema:
        return ConnectionNodeUpdateSchema.model_validate(self.model_dump())


def get_connection_node_get_all_params() -> ConnectionNodeGetAllParams:
    return ConnectionNodeGetAllParams()


def get_connection_node_paginated_params(
    page: int = Query(1, description="Номер страницы", ge=1),
    limit: int = Query(10, description="Количество записей на странице", ge=1, le=100),
) -> ConnectionNodePaginatedParams:
    return ConnectionNodePaginatedParams(page=page, limit=limit)


def get_connection_node_get_params(
    id: int = Path(..., description="Идентификатор соединения узлов", ge=1),
) -> ConnectionNodeGetParams:
    return ConnectionNodeGetParams(id=id)


def get_connection_node_delete_params(
    id: int = Path(..., description="Идентификатор соединения узлов", ge=1),
) -> ConnectionNodeDeleteParams:
    return ConnectionNodeDeleteParams(id=id)


def get_connection_node_create_params(
    node_id1: int = Body(..., description="Идентификатор первого узла"),
    node_id2: int = Body(..., description="Идентификатор второго узла"),
    connection_type_id: int | None = Body(None, description="Идентификатор типа соединения"),
    distance: float = Body(..., description="Расстояние между узлами"),
) -> ConnectionNodeCreateParams:
    return ConnectionNodeCreateParams(
        node_id1=node_id1,
        node_id2=node_id2,
        connection_type_id=connection_type_id,
        distance=distance,
    )


def get_connection_node_update_params(
    id: int = Path(..., description="Идентификатор соединения узлов", ge=1),
    node_id1: int | None = Body(None, description="Идентификатор первого узла"),
    node_id2: int | None = Body(None, description="Идентификатор второго узла"),
    connection_type_id: int | None = Body(None, description="Идентификатор типа соединения"),
    distance: float | None = Body(None, description="Расстояние между узлами"),
) -> ConnectionNodeUpdateParams:
    return ConnectionNodeUpdateParams(
        id=id,
        node_id1=node_id1,
        node_id2=node_id2,
        connection_type_id=connection_type_id,
        distance=distance,
    )