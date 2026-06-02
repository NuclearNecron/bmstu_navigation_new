from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any


class NodeTypeSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    uni: Optional[int] = None
    campus: Optional[int] = None
    complex: Optional[int] = None
    corpus: Optional[int] = None
    building: Optional[int] = None
    floor: Optional[int] = None
    transit: Optional[int] = None
    room: Optional[int] = None
    exit_point: Optional[int] = None


class NodeTypesSchema(BaseModel):
    node_types: dict[int, NodeTypeSchema]


class NodeSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    type_id: int
    x: float
    y: float
    z: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    name: str


class NodesSchema(BaseModel):
    nodes: dict[int, NodeSchema]


class ConnectionSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    distance: float
    node1_id: int
    node2_id: int


class ConnectionsSchema(BaseModel):
    nodes: dict[int, dict[int, ConnectionSchema]]


class ChangeNodeSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    type_id: Optional[int] = None
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    name: Optional[str] = None


class ChangeNodeTypeSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    uni: Optional[int] = None
    campus: Optional[int] = None
    complex: Optional[int] = None
    corpus: Optional[int] = None
    building: Optional[int] = None
    floor: Optional[int] = None
    transit: Optional[int] = None
    room: Optional[int] = None
    exit_point: Optional[int] = None


class ChangeConnectionSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    distance: Optional[float] = None
