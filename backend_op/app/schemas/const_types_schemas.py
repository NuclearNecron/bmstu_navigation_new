from pydantic import BaseModel


class ObjectTypeSchema(BaseModel):
    id: int
    parent_id: int | None
    number: int | None
    short_name: str | None
    full_name: str | None
    description: str | None
    colour: str | None


class ObjectKindSchema(BaseModel):
    id: int
    parent_id: int | None
    type_id: int
    number: int
    short_name: str
    full_name: str
    description: str | None
    colour: str


class ObjectStateSchema(BaseModel):
    id: int
    number: int
    short_name: str
    full_name: str
    description: str | None
    colour: str


class ConnectionTypeSchema(BaseModel):
    id: int
    number: int
    short_name: str
    full_name: str
    description: str | None
    colour: str
    style: str | None
