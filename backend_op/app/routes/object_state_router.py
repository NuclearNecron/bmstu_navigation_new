from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.handlers.object_state_handler import ObjectStateHandler
from app.params.object_state_params import (
    ObjectStateCreateParams,
    ObjectStateDeleteParams,
    ObjectStateGetAllParams,
    ObjectStateGetParams,
    ObjectStatePaginatedParams,
    ObjectStateUpdateParams,
    get_object_state_create_params,
    get_object_state_delete_params,
    get_object_state_get_all_params,
    get_object_state_get_params,
    get_object_state_paginated_params,
    get_object_state_update_params,
)
from app.schemas.const_types_schemas import ObjectStateSchema

router = APIRouter(
    prefix="/object-states",
    tags=["object-states"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Depends(get_session)


@router.get("/", response_model=list[ObjectStateSchema])
async def get_all_object_states(
    session: AsyncSession = SessionDep,
    params: ObjectStateGetAllParams = Depends(get_object_state_get_all_params),
):
    """
    Получить список всех состояний объектов.
    """
    handler = ObjectStateHandler()
    result = await handler.get_all(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/page", response_model=list[ObjectStateSchema])
async def get_paginated_object_states(
    session: AsyncSession = SessionDep,
    params: ObjectStatePaginatedParams = Depends(get_object_state_paginated_params),
):
    """
    Получить список состояний объектов с пагинацией.
    """
    handler = ObjectStateHandler()
    result = await handler.get_paginated(session, params.to_pagination())
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/{id}", response_model=ObjectStateSchema)
async def get_object_state(
    session: AsyncSession = SessionDep,
    params: ObjectStateGetParams = Depends(get_object_state_get_params),
) -> ObjectStateSchema | None:
    """
    Получить состояние объекта по ID.
    """
    handler = ObjectStateHandler()
    result = await handler.get(session, params.to_get_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Object state not found")
    return JSONResponse(content=result.model_dump())



@router.post("/", response_model=ObjectStateSchema, status_code=status.HTTP_201_CREATED)
async def create_object_state(
    session: AsyncSession = SessionDep,
    params: ObjectStateCreateParams = Depends(get_object_state_create_params),
) -> ObjectStateSchema:
    """
    Создать новое состояние объекта.
    """
    handler = ObjectStateHandler()
    result = await handler.create(session, params.to_create_schema())
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)


@router.put("/{id}", response_model=ObjectStateSchema)
async def update_object_state(
    session: AsyncSession = SessionDep,
    params: ObjectStateUpdateParams = Depends(get_object_state_update_params),
) -> ObjectStateSchema | None:
    """
    Обновить состояние объекта по ID.
    """
    handler = ObjectStateHandler()
    
    # Проверяем существование обновляемого объекта
    existing = await handler.get(session, params.id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Object state not found")
    
    result = await handler.update(session, params.to_edit_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Object state not found")
    return JSONResponse(content=result.model_dump())



@router.delete("/{id}", response_model=dict)
async def delete_object_state(
    session: AsyncSession = SessionDep,
    params: ObjectStateDeleteParams = Depends(get_object_state_delete_params),
) -> dict:
    """
    Удалить состояние объекта по ID.
    """
    handler = ObjectStateHandler()
    deleted = await handler.delete(session, params.to_delete_schema())
    if not deleted:
        raise HTTPException(status_code=404, detail="Object state not found")
    return JSONResponse(content={"status": "success", "message": "Object state deleted"})