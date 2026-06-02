from pydantic import BaseModel

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



class NodeDeleteParams(BaseModel):
    """Параметры для удаления узла."""

    id: int