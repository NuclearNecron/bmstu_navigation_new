from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.handlers.connection_object_handler import ConnectionObjectHandler
from app.handlers.object_handler import ObjectHandler
from app.handlers.connection_type_handler import ConnectionTypeHandler
from app.params.connection_object_params import (
    ConnectionObjectCreateParams,
    ConnectionObjectDeleteParams,
    ConnectionObjectGetAllParams,
    ConnectionObjectGetParams,
    ConnectionObjectPaginatedParams,
    ConnectionObjectUpdateParams,
    get_connection_object_create_params,
    get_connection_object_delete_params,
    get_connection_object_get_all_params,
    get_connection_object_get_params,
    get_connection_object_paginated_params,
    get_connection_object_update_params,
)
from app.schemas.object_models_schemas import ConnectionObjectSchema

router = APIRouter(
    prefix="/connection-objects",
    tags=["connection-objects"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Depends(get_session)


async def validate_object_exists(object_id: int, session: AsyncSession):
    """Проверяет существование объекта."""
    handler = ObjectHandler()
    obj = await handler.get(session, object_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Object with id {object_id} not found",
        )
    return True


async def validate_connection_type_exists(
    connection_type_id: int, session: AsyncSession
):
    """Проверяет существование типа соединения. Если connection_type_id is None, возвращает True."""
    if connection_type_id is None:
        return True

    handler = ConnectionTypeHandler()
    conn_type = await handler.get(session, connection_type_id)
    if conn_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Connection type with id {connection_type_id} not found",
        )
    return True


@router.get("/", response_model=list[ConnectionObjectSchema])
async def get_all_connection_objects(
    session: AsyncSession = SessionDep,
    params: ConnectionObjectGetAllParams = Depends(
        get_connection_object_get_all_params
    ),
):
    """
    Получить список всех соединений объектов.
    """
    handler = ConnectionObjectHandler()
    result = await handler.get_all(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/page", response_model=list[ConnectionObjectSchema])
async def get_paginated_connection_objects(
    session: AsyncSession = SessionDep,
    params: ConnectionObjectPaginatedParams = Depends(
        get_connection_object_paginated_params
    ),
):
    """
    Получить список соединений объектов с пагинацией.
    """
    handler = ConnectionObjectHandler()
    result = await handler.get_paginated(session, params.to_pagination())
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/{id}", response_model=ConnectionObjectSchema)
async def get_connection_object(
    session: AsyncSession = SessionDep,
    params: ConnectionObjectGetParams = Depends(get_connection_object_get_params),
) -> ConnectionObjectSchema | None:
    """
    Получить соединение объектов по ID.
    """
    handler = ConnectionObjectHandler()
    result = await handler.get(session, params.to_get_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Connection object not found")
    return JSONResponse(content=result.model_dump())


@router.post(
    "/", response_model=ConnectionObjectSchema, status_code=status.HTTP_201_CREATED
)
async def create_connection_object(
    session: AsyncSession = SessionDep,
    params: ConnectionObjectCreateParams = Depends(get_connection_object_create_params),
) -> ConnectionObjectSchema:
    """
    Создать новое соединение объектов.
    """
    handler = ConnectionObjectHandler()

    # Проверяем существование первого объекта
    await validate_object_exists(params.object_id1, session)

    # Проверяем существование второго объекта
    await validate_object_exists(params.object_id2, session)

    # Проверяем существование типа соединения
    await validate_connection_type_exists(params.connection_type_id, session)

    result = await handler.create(session, params.to_create_schema())
    return JSONResponse(
        content=result.model_dump(), status_code=status.HTTP_201_CREATED
    )


@router.put("/{id}", response_model=ConnectionObjectSchema)
async def update_connection_object(
    session: AsyncSession = SessionDep,
    params: ConnectionObjectUpdateParams = Depends(get_connection_object_update_params),
) -> ConnectionObjectSchema | None:
    """
    Обновить соединение объектов по ID.
    """
    handler = ConnectionObjectHandler()

    # Проверяем существование обновляемого объекта
    existing = await handler.get(session, params.id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Connection object not found")

    # Проверяем существование первого объекта, если он указан
    if params.object_id1 is not None:
        await validate_object_exists(params.object_id1, session)

    # Проверяем существование второго объекта, если он указан
    if params.object_id2 is not None:
        await validate_object_exists(params.object_id2, session)

    # Проверяем существование типа соединения, если он указан
    if params.connection_type_id is not None:
        await validate_connection_type_exists(params.connection_type_id, session)

    result = await handler.update(session, params.to_edit_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Connection object not found")
    return JSONResponse(content=result.model_dump())


@router.delete("/{id}", response_model=dict)
async def delete_connection_object(
    session: AsyncSession = SessionDep,
    params: ConnectionObjectDeleteParams = Depends(get_connection_object_delete_params),
) -> dict:
    """
    Удалить соединение объектов по ID.
    """
    handler = ConnectionObjectHandler()
    deleted = await handler.delete(session, params.to_delete_schema())
    if not deleted:
        raise HTTPException(status_code=404, detail="Connection object not found")
    return JSONResponse(
        content={"status": "success", "message": "Connection object deleted"}
    )
