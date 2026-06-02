from fastapi import Body, Path, Query
from pydantic import BaseModel

from app.base.base_schemas import DeleteSchema, GetSchema, Pagination
from app.schemas.object_models_schemas import (
    ConnectionObjectCreateSchema,
    ConnectionObjectUpdateSchema,
)


class ConnectionObjectGetAllParams(BaseModel):
    """Запрос списка всех соединений объектов (без параметров)."""


class ConnectionObjectPaginatedParams(BaseModel):
    page: int
    limit: int

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, limit=self.limit)


class ConnectionObjectGetParams(BaseModel):
    id: int

    def to_get_schema(self) -> GetSchema:
        return GetSchema(id=self.id)


class ConnectionObjectDeleteParams(BaseModel):
    id: int

    def to_delete_schema(self) -> DeleteSchema:
        return DeleteSchema(id=self.id)


class ConnectionObjectCreateParams(BaseModel):
    object_id1: int
    object_id2: int
    connection_type_id: int | None = None
    distance: float

    def to_create_schema(self) -> ConnectionObjectCreateSchema:
        return ConnectionObjectCreateSchema.model_validate(self.model_dump())


class ConnectionObjectUpdateParams(BaseModel):
    id: int
    object_id1: int | None = None
    object_id2: int | None = None
    connection_type_id: int | None = None
    distance: float | None = None

    def to_edit_schema(self) -> ConnectionObjectUpdateSchema:
        return ConnectionObjectUpdateSchema.model_validate(self.model_dump())


def get_connection_object_get_all_params() -> ConnectionObjectGetAllParams:
    return ConnectionObjectGetAllParams()


def get_connection_object_paginated_params(
    page: int = Query(1, description="Номер страницы", ge=1),
    limit: int = Query(10, description="Количество записей на странице", ge=1, le=100),
) -> ConnectionObjectPaginatedParams:
    return ConnectionObjectPaginatedParams(page=page, limit=limit)


def get_connection_object_get_params(
    id: int = Path(..., description="Идентификатор соединения объектов", ge=1),
) -> ConnectionObjectGetParams:
    return ConnectionObjectGetParams(id=id)


def get_connection_object_delete_params(
    id: int = Path(..., description="Идентификатор соединения объектов", ge=1),
) -> ConnectionObjectDeleteParams:
    return ConnectionObjectDeleteParams(id=id)


def get_connection_object_create_params(
    object_id1: int = Body(..., description="Идентификатор первого объекта"),
    object_id2: int = Body(..., description="Идентификатор второго объекта"),
    connection_type_id: int | None = Body(
        None, description="Идентификатор типа соединения"
    ),
    distance: float = Body(..., description="Расстояние между объектами"),
) -> ConnectionObjectCreateParams:
    return ConnectionObjectCreateParams(
        object_id1=object_id1,
        object_id2=object_id2,
        connection_type_id=connection_type_id,
        distance=distance,
    )


def get_connection_object_update_params(
    id: int = Path(..., description="Идентификатор соединения объектов", ge=1),
    object_id1: int | None = Body(None, description="Идентификатор первого объекта"),
    object_id2: int | None = Body(None, description="Идентификатор второго объекта"),
    connection_type_id: int | None = Body(
        None, description="Идентификатор типа соединения"
    ),
    distance: float | None = Body(None, description="Расстояние между объектами"),
) -> ConnectionObjectUpdateParams:
    return ConnectionObjectUpdateParams(
        id=id,
        object_id1=object_id1,
        object_id2=object_id2,
        connection_type_id=connection_type_id,
        distance=distance,
    )
