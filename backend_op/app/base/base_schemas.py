from pydantic import BaseModel


class DeleteSchema(BaseModel):
    id: int


class GetSchema(BaseModel):
    id: int


class Pagination(BaseModel):
    page: int
    limit: int
