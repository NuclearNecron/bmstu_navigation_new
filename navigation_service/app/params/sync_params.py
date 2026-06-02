from fastapi import Body, Path
from pydantic import BaseModel

from app.schemas.map_schemas import (
    NodeTypeSchema, 
    NodeSchema, 
    ConnectionSchema,
    ChangeNodeTypeSchema,
    ChangeNodeSchema,
    ChangeConnectionSchema
)

# === Параметры для операций с типами узлов (NodeType) ===

class NodeTypeCreateParams(BaseModel):
    """Параметры для создания типа узла."""
    id: int
    uni: int | None = None
    campus: int | None = None
    complex: int | None = None
    corpus: int | None = None
    building: int | None = None
    floor: int | None = None
    transit: int | None = None
    room: int | None = None
    exit_point: int | None = None

    def to_create_schema(self) -> NodeTypeSchema:
        return NodeTypeSchema.model_validate(self.model_dump())


class NodeTypeUpdateParams(BaseModel):
    """Параметры для обновления типа узла."""
    id: int
    uni: int | None = None
    campus: int | None = None
    complex: int | None = None
    corpus: int | None = None
    building: int | None = None
    floor: int | None = None
    transit: int | None = None
    room: int | None = None
    exit_point: int | None = None

    def to_update_schema(self) -> ChangeNodeTypeSchema:
        return ChangeNodeTypeSchema.model_validate(self.model_dump())


class NodeTypeDeleteParams(BaseModel):
    """Параметры для удаления типа узла."""
    id: int

# === Параметры для операций с узлами (Node) ===

class NodeCreateParams(BaseModel):
    """Параметры для создания узла."""
    id: int
    type_id: int
    x: float
    y: float
    z: float
    latitude: float | None = None
    longitude: float | None = None
    name: str

    def to_create_schema(self) -> NodeSchema:
        return NodeSchema.model_validate(self.model_dump())


class NodeUpdateParams(BaseModel):
    """Параметры для обновления узла."""
    id: int
    type_id: int | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    name: str | None = None

    def to_update_schema(self) -> ChangeNodeSchema:
        return ChangeNodeSchema.model_validate(self.model_dump())


class NodeDeleteParams(BaseModel):
    """Параметры для удаления узла."""
    id: int

# === Параметры для операций с связями (Connection) ===

class ConnectionCreateParams(BaseModel):
    """Параметры для создания связи."""
    id: int
    distance: float
    node1_id: int
    node2_id: int

    def to_create_schema(self) -> ConnectionSchema:
        return ConnectionSchema.model_validate(self.model_dump())


class ConnectionUpdateParams(BaseModel):
    """Параметры для обновления связи."""
    id: int
    distance: float | None = None

    def to_update_schema(self) -> ChangeConnectionSchema:
        return ChangeConnectionSchema.model_validate(self.model_dump())


class ConnectionDeleteParams(BaseModel):
    """Параметры для удаления связи."""
    id: int

# === Зависимости для внедрения параметров ===

def get_node_type_create_params(
    id: int = Body(..., description="Идентификатор типа узла"),
    uni: int | None = Body(None, description="Идентификатор университета"),
    campus: int | None = Body(None, description="Идентификатор кампуса"),
    complex: int | None = Body(None, description="Идентификатор комплекса"),
    corpus: int | None = Body(None, description="Идентификатор корпуса"),
    building: int | None = Body(None, description="Идентификатор здания"),
    floor: int | None = Body(None, description="Идентификатор этажа"),
    transit: int | None = Body(None, description="Идентификатор перехода"),
    room: int | None = Body(None, description="Идентификатор помещения"),
    exit_point: int | None = Body(None, description="Идентификатор точки выхода"),
) -> NodeTypeCreateParams:
    return NodeTypeCreateParams(
        id=id,
        uni=uni,
        campus=campus,
        complex=complex,
        corpus=corpus,
        building=building,
        floor=floor,
        transit=transit,
        room=room,
        exit_point=exit_point,
    )

def get_node_type_update_params(
    id: int = Path(..., description="Идентификатор типа узла", ge=1),
    uni: int | None = Body(None, description="Идентификатор университета"),
    campus: int | None = Body(None, description="Идентификатор кампуса"),
    complex: int | None = Body(None, description="Идентификатор комплекса"),
    corpus: int | None = Body(None, description="Идентификатор корпуса"),
    building: int | None = Body(None, description="Идентификатор здания"),
    floor: int | None = Body(None, description="Идентификатор этажа"),
    transit: int | None = Body(None, description="Идентификатор перехода"),
    room: int | None = Body(None, description="Идентификатор помещения"),
    exit_point: int | None = Body(None, description="Идентификатор точки выхода"),
) -> NodeTypeUpdateParams:
    return NodeTypeUpdateParams(
        id=id,
        uni=uni,
        campus=campus,
        complex=complex,
        corpus=corpus,
        building=building,
        floor=floor,
        transit=transit,
        room=room,
        exit_point=exit_point,
    )

def get_node_type_delete_params(
    id: int = Path(..., description="Идентификатор типа узла", ge=1),
) -> NodeTypeDeleteParams:
    return NodeTypeDeleteParams(id=id)

def get_node_create_params(
    id: int = Body(..., description="Идентификатор узла"),
    type_id: int = Body(..., description="Идентификатор типа узла"),
    x: float = Body(..., description="Координата X"),
    y: float = Body(..., description="Координата Y"),
    z: float = Body(..., description="Координата Z"),
    latitude: float | None = Body(None, description="Широта"),
    longitude: float | None = Body(None, description="Долгота"),
    name: str = Body(..., description="Название узла"),
) -> NodeCreateParams:
    return NodeCreateParams(
        id=id,
        type_id=type_id,
        x=x,
        y=y,
        z=z,
        latitude=latitude,
        longitude=longitude,
        name=name,
    )

def get_node_update_params(
    id: int = Path(..., description="Идентификатор узла", ge=1),
    type_id: int | None = Body(None, description="Идентификатор типа узла"),
    x: float | None = Body(None, description="Координата X"),
    y: float | None = Body(None, description="Координата Y"),
    z: float | None = Body(None, description="Координата Z"),
    latitude: float | None = Body(None, description="Широта"),
    longitude: float | None = Body(None, description="Долгота"),
    name: str | None = Body(None, description="Название узла"),
) -> NodeUpdateParams:
    return NodeUpdateParams(
        id=id,
        type_id=type_id,
        x=x,
        y=y,
        z=z,
        latitude=latitude,
        longitude=longitude,
        name=name,
    )

def get_node_delete_params(
    id: int = Path(..., description="Идентификатор узла", ge=1),
) -> NodeDeleteParams:
    return NodeDeleteParams(id=id)

def get_connection_create_params(
    id: int = Body(..., description="Идентификатор связи"),
    distance: float = Body(..., description="Дистанция между узлами"),
    node1_id: int = Body(..., description="Идентификатор первого узла"),
    node2_id: int = Body(..., description="Идентификатор второго узла"),
) -> ConnectionCreateParams:
    return ConnectionCreateParams(
        id=id,
        distance=distance,
        node1_id=node1_id,
        node2_id=node2_id,
    )

def get_connection_update_params(
    id: int = Path(..., description="Идентификатор связи", ge=1),
    distance: float | None = Body(None, description="Дистанция между узлами"),
) -> ConnectionUpdateParams:
    return ConnectionUpdateParams(id=id, distance=distance)

def get_connection_delete_params(
    id: int = Path(..., description="Идентификатор связи", ge=1),
) -> ConnectionDeleteParams:
    return ConnectionDeleteParams(id=id)