from pydantic import BaseModel, ConfigDict


class NodeTypeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    short_name: str
    full_name: str
    description: str | None
    colour: str
    size: float


class NodeTypeCreateSchema(BaseModel):
    short_name: str
    full_name: str
    description: str | None = None
    colour: str
    size: float


class NodeTypeUpdateSchema(BaseModel):
    id: int
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None
    size: float | None = None


class NodeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: int | None
    object_id: int
    type_id: int
    short_name: str
    full_name: str
    SVG: str | None
    x: float | None
    y: float | None
    z: float | None
    latitude: float | None
    longitude: float | None


class NodeMapperSchema(BaseModel):

    id: int
    object_id: int
    short_name: str
    x: float | None
    y: float | None
    z: float | None
    latitude: float | None
    longitude: float | None


class NodeCreateSchema(BaseModel):
    parent_id: int | None = None
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


class NodeUpdateSchema(BaseModel):
    id: int
    parent_id: int | None = None
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


class ConnectionNodeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    node_id1: int
    node_id2: int
    connection_type_id: int | None
    distance: float


class ConnectionNodeCreateSchema(BaseModel):
    node_id1: int
    node_id2: int
    connection_type_id: int | None = None
    distance: float


class ConnectionNodeUpdateSchema(BaseModel):
    id: int
    node_id1: int | None = None
    node_id2: int | None = None
    connection_type_id: int | None = None
    distance: float | None = None


class NodeNavSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    type_id: int
    x: float
    y: float
    z: float
    latitude: float | None = None
    longitude: float | None = None
    name: str


class ConnectionNodeNavSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    node_id1: int
    node_id2: int
    distance: float


class ConnectionNodeNavUpdSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    distance: float
