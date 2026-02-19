from pydantic import BaseModel


class ObjectSchema(BaseModel):
    id: int
    parent_id: int | None
    kind_id: int
    state_id: int
    number: int
    short_name: str
    full_name: str
    description: str | None
    address: str | None
    plan_link: str | None
    blueprint_link: str | None
    scale: str | None
    height: float | None
    SVG: str | None


class ConnectionObjectSchema(BaseModel):
    id: int
    object_id1: int
    object_id2: int
    connection_type_id: int | None
    distance: float
