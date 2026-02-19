from pydantic import BaseModel


class NodeTypeSchema(BaseModel):
    id: int
    number: int
    short_name: str
    full_name: str
    description: str | None
    colour: str
    size: float


class NodeSchema(BaseModel):
    id: int
    parent_id: int | None
    object_id: int
    type_id: int
    number: int
    short_name: str
    full_name: str
    SVG: str | None
    x: float | None
    y: float | None
    z: float | None


class ConnectionNodeSchema(BaseModel):
    id: int
    node_id1: int
    node_id2: int
    connection_type_id: int | None
    distance: float
