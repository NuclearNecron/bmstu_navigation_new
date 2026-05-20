from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.handlers.connection_type_handler import ConnectionTypeHandler
from app.params.connection_type_params import (
    ConnectionTypeCreateParams,
    ConnectionTypeDeleteParams,
    ConnectionTypeGetAllParams,
    ConnectionTypeGetParams,
    ConnectionTypePaginatedParams,
    ConnectionTypeUpdateParams,
    get_connection_type_create_params,
    get_connection_type_delete_params,
    get_connection_type_get_all_params,
    get_connection_type_get_params,
    get_connection_type_paginated_params,
    get_connection_type_update_params,
)
from app.schemas.const_types_schemas import ConnectionTypeSchema

router = APIRouter(
    prefix="/connection-types",
    tags=["connection-types"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Depends(get_session)


@router.get("/", response_model=list[ConnectionTypeSchema])
async def get_all_connection_types(
    session: AsyncSession = SessionDep,
    params: ConnectionTypeGetAllParams = Depends(get_connection_type_get_all_params),
):
    """
    Получить список всех типов соединений.
    """
    handler = ConnectionTypeHandler()
    result = await handler.get_all(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/page", response_model=list[ConnectionTypeSchema])
async def get_paginated_connection_types(
    session: AsyncSession = SessionDep,
    params: ConnectionTypePaginatedParams = Depends(get_connection_type_paginated_params),
):
    """
    Получить список типов соединений с пагинацией.
    """
    handler = ConnectionTypeHandler()
    result = await handler.get_paginated(session, params.to_pagination())
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/{id}", response_model=ConnectionTypeSchema)
async def get_connection_type(
    session: AsyncSession = SessionDep,
    params: ConnectionTypeGetParams = Depends(get_connection_type_get_params),
) -> ConnectionTypeSchema | None:
    """
    Получить тип соединения по ID.
    """
    handler = ConnectionTypeHandler()
    result = await handler.get(session, params.to_get_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Connection type not found")
    return JSONResponse(content=result.model_dump())



@router.post("/", response_model=ConnectionTypeSchema, status_code=status.HTTP_201_CREATED)
async def create_connection_type(
    session: AsyncSession = SessionDep,
    params: ConnectionTypeCreateParams = Depends(get_connection_type_create_params),
) -> ConnectionTypeSchema:
    """
    Создать новый тип соединения.
    """
    handler = ConnectionTypeHandler()
    result = await handler.create(session, params.to_create_schema())
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)


@router.put("/{id}", response_model=ConnectionTypeSchema)
async def update_connection_type(
    session: AsyncSession = SessionDep,
    params: ConnectionTypeUpdateParams = Depends(get_connection_type_update_params),
) -> ConnectionTypeSchema | None:
    """
    Обновить тип соединения по ID.
    """
    handler = ConnectionTypeHandler()
    
    # Проверяем существование обновляемого объекта
    existing = await handler.get(session, params.id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Connection type not found")
    
    result = await handler.update(session, params.to_edit_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Connection type not found")
    return JSONResponse(content=result.model_dump())



@router.delete("/{id}", response_model=dict)
async def delete_connection_type(
    session: AsyncSession = SessionDep,
    params: ConnectionTypeDeleteParams = Depends(get_connection_type_delete_params),
) -> dict:
    """
    Удалить тип соединения по ID.
    """
    handler = ConnectionTypeHandler()
    deleted = await handler.delete(session, params.to_delete_schema())
    if not deleted:
        raise HTTPException(status_code=404, detail="Connection type not found")
    return JSONResponse(content={"status": "success", "message": "Connection type deleted"})