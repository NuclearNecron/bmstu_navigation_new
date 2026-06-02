from pydantic import BaseModel

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




class NodeTypeDeleteParams(BaseModel):
    """Параметры для удаления типа узла."""

    id: int