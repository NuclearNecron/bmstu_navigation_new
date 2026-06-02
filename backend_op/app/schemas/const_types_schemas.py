from pydantic import BaseModel, ConfigDict


class ObjectTypeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    parent_id: int | None
    short_name: str
    full_name: str
    description: str | None
    colour: str


class ObjectTypeCreateSchema(BaseModel):
    parent_id: int | None = None
    short_name: str
    full_name: str
    description: str | None = None
    colour: str


class ObjectTypeEditSchema(BaseModel):
    id: int
    parent_id: int | None = None
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None


class ObjectKindSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: int | None
    type_id: int
    short_name: str
    full_name: str
    description: str | None
    colour: str


class ObjectKindCreateSchema(BaseModel):
    parent_id: int | None = None
    type_id: int
    short_name: str
    full_name: str
    description: str | None = None
    colour: str


class ObjectKindUpdateSchema(BaseModel):
    id: int
    parent_id: int | None = None
    type_id: int | None = None
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None


class ObjectStateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    short_name: str
    full_name: str
    description: str | None
    colour: str


class ObjectStateCreateSchema(BaseModel):

    short_name: str
    full_name: str
    description: str | None = None
    colour: str


class ObjectStateUpdateSchema(BaseModel):
    id: int
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None


class ConnectionTypeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    short_name: str
    full_name: str
    description: str | None
    colour: str
    style: str | None


class ConnectionTypeCreateSchema(BaseModel):
    short_name: str
    full_name: str
    description: str | None = None
    colour: str
    style: str | None = None


class ConnectionTypeUpdateSchema(BaseModel):
    id: int
    short_name: str | None = None
    full_name: str | None = None
    description: str | None = None
    colour: str | None = None
    style: str | None = None
