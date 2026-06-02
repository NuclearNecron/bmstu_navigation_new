from pydantic import BaseModel

class ConnectionCreateParams(BaseModel):
    """Параметры для создания связи."""

    id: int
    distance: float
    node1_id: int
    node2_id: int


class ConnectionUpdateParams(BaseModel):
    """Параметры для обновления связи."""

    id: int
    distance: float | None = None


class ConnectionDeleteParams(BaseModel):
    """Параметры для удаления связи."""

    id: int