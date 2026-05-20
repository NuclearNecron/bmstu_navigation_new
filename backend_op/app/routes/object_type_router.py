from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.handlers.object_type_handler import ObjectTypeHandler
from app.params.object_type_params import (
    ObjectTypeCreateParams,
    ObjectTypeDeleteParams,
    ObjectTypeGetAllParams,
    ObjectTypeGetChildrenParams,
    ObjectTypeGetParams,
    ObjectTypePaginatedParams,
    ObjectTypeUpdateParams,
    get_object_type_create_params,
    get_object_type_delete_params,
    get_object_type_get_all_params,
    get_object_type_get_children_params,
    get_object_type_get_params,
    get_object_type_paginated_params,
    get_object_type_update_params,
)
from app.schemas.const_types_schemas import ObjectTypeSchema

router = APIRouter(
    prefix="/object-types",
    tags=["object-types"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Depends(get_session)


async def validate_parent_exists(parent_id: int, handler: ObjectTypeHandler, session: AsyncSession):
    """Проверяет существование родительского объекта."""
    if parent_id is None:
        return True
    
    parent = await handler.get(session, parent_id)
    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Parent object type with id {parent_id} not found"
        )
    return True


async def validate_type_exists(type_id: int, handler: ObjectTypeHandler, session: AsyncSession):
    """Проверяет существование типа объекта."""
    obj_type = await handler.get(session, type_id)
    if obj_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Object type with id {type_id} not found"
        )
    return True


@router.get("/", response_model=list[ObjectTypeSchema])
async def get_all_object_types(
    session: AsyncSession = SessionDep,
    params: ObjectTypeGetAllParams = Depends(get_object_type_get_all_params),
):
    """
    Получить список всех типов объектов.
    """
    handler = ObjectTypeHandler()
    result = await handler.get_all(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/page", response_model=list[ObjectTypeSchema])
async def get_paginated_object_types(
    session: AsyncSession = SessionDep,
    params: ObjectTypePaginatedParams = Depends(get_object_type_paginated_params),
):
    """
    Получить список типов объектов с пагинацией.
    """
    handler = ObjectTypeHandler()
    result = await handler.get_paginated(session, params.to_pagination())
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/{id}", response_model=ObjectTypeSchema)
async def get_object_type(
    session: AsyncSession = SessionDep,
    params: ObjectTypeGetParams = Depends(get_object_type_get_params),
) -> ObjectTypeSchema | None:
    """
    Получить тип объекта по ID.
    """
    handler = ObjectTypeHandler()
    result = await handler.get(session, params.to_get_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Object type not found")
    return JSONResponse(content=result.model_dump())


@router.post("/", response_model=ObjectTypeSchema, status_code=status.HTTP_201_CREATED)
async def create_object_type(
    session: AsyncSession = SessionDep,
    params: ObjectTypeCreateParams = Depends(get_object_type_create_params),
) -> ObjectTypeSchema:
    """
    Создать новый тип объекта.
    """
    handler = ObjectTypeHandler()
    
    # Проверяем существование родительского объекта
    if params.parent_id is not None:
        await validate_parent_exists(params.parent_id, handler, session)
    
    result = await handler.create(session, params.to_create_schema())
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)


@router.put("/{id}", response_model=ObjectTypeSchema)
async def update_object_type(
    session: AsyncSession = SessionDep,
    params: ObjectTypeUpdateParams = Depends(get_object_type_update_params),
) -> ObjectTypeSchema | None:
    """
    Обновить тип объекта по ID.
    """
    handler = ObjectTypeHandler()
    
    # Проверяем существование обновляемого объекта
    existing = await handler.get(session, params.id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Object type not found")
    
    # Проверяем существование родительского объекта, если он указан
    if params.parent_id is not None:
        await validate_parent_exists(params.parent_id, handler, session)
    
    result = await handler.update(session, params.to_edit_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Object type not found")
    return JSONResponse(content=result.model_dump())



@router.delete("/{id}", response_model=dict)
async def delete_object_type(
    session: AsyncSession = SessionDep,
    params: ObjectTypeDeleteParams = Depends(get_object_type_delete_params),
) -> dict:
    """
    Удалить тип объекта по ID.
    """
    handler = ObjectTypeHandler()
    deleted = await handler.delete(session, params.to_delete_schema())
    if not deleted:
        raise HTTPException(status_code=404, detail="Object type not found")
    return JSONResponse(content={"status": "success", "message": "Object type deleted"})



@router.get("/parent/{parent_id}", response_model=list[ObjectTypeSchema])
async def get_object_types_by_parent(
    session: AsyncSession = SessionDep,
    params: ObjectTypeGetChildrenParams = Depends(get_object_type_get_children_params),
) -> list[ObjectTypeSchema]:
    """
    Получить список дочерних типов объектов по parent_id.
    """
    handler = ObjectTypeHandler()
    result = await handler.get_children_by_parent(session, params.parent_id)
    return JSONResponse(content=[obj.model_dump() for obj in result])