from pydantic import BaseModel, ConfigDict


class ObjectSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: int | None
    kind_id: int
    state_id: int
    short_name: str
    full_name: str
    description: str | None
    address: str | None
    plan_link: str | None
    blueprint_link: str | None
    scale: str | None
    height: float | None
    SVG: str | None


class ObjectMapperSchema(BaseModel):

    id: int
    parent_id: int | None


class ObjectCreateSchema(BaseModel):
    parent_id: int | None = None
    kind_id: int
    state_id: int
    short_name: str
    full_name: str
    description: str | None = None
    address: str | None = None
    plan_link: str | None = None
    blueprint_link: str | None = None
    scale: str | None = None
    height: float | None = None
    SVG: str | None = None


class ObjectUpdateSchema(BaseModel):
    id: int
    parent_id: int | None = None
    kind_id: int | None = None
    state_id: int | None = None
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    address: str | None = None
    plan_link: str | None = None
    blueprint_link: str | None = None
    scale: str | None = None
    height: float | None = None
    SVG: str | None = None


class ConnectionObjectSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    object_id1: int
    object_id2: int
    connection_type_id: int | None
    distance: float


class ConnectionObjectCreateSchema(BaseModel):
    object_id1: int
    object_id2: int
    connection_type_id: int | None = None
    distance: float


class ConnectionObjectUpdateSchema(BaseModel):
    id: int
    object_id1: int | None = None
    object_id2: int | None = None
    connection_type_id: int | None = None
    distance: float | None = None


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
