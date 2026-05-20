from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.handlers.object_kind_handler import ObjectKindHandler
from app.handlers.object_type_handler import ObjectTypeHandler
from app.params.object_kind_params import (
    ObjectKindCreateParams,
    ObjectKindDeleteParams,
    ObjectKindGetAllParams,
    ObjectKindGetChildrenParams,
    ObjectKindGetParams,
    ObjectKindPaginatedParams,
    ObjectKindUpdateParams,
    get_object_kind_create_params,
    get_object_kind_delete_params,
    get_object_kind_get_all_params,
    get_object_kind_get_children_params,
    get_object_kind_get_params,
    get_object_kind_paginated_params,
    get_object_kind_update_params,
)
from app.schemas.const_types_schemas import ObjectKindSchema

router = APIRouter(
    prefix="/object-kinds",
    tags=["object-kinds"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Depends(get_session)


async def validate_parent_exists(parent_id: int, handler: ObjectKindHandler, session: AsyncSession):
    """Проверяет существование родительского объекта."""
    if parent_id is None:
        return True
    
    parent = await handler.get(session, parent_id)
    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Parent object kind with id {parent_id} not found"
        )
    return True

async def validate_type_exists(type_id: int, session: AsyncSession):
    """Проверяет существование типа объекта. Если type_id is None, возвращает True."""
    if type_id is None:
        return True
        
    handler = ObjectTypeHandler()
    obj_type = await handler.get(session, type_id)
    if obj_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Object type with id {type_id} not found"
        )
    return True


@router.get("/", response_model=list[ObjectKindSchema])
async def get_all_object_kinds(
    session: AsyncSession = SessionDep,
    params: ObjectKindGetAllParams = Depends(get_object_kind_get_all_params),
):
    """
    Получить список всех видов объектов.
    """
    handler = ObjectKindHandler()
    result = await handler.get_all(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/page", response_model=list[ObjectKindSchema])
async def get_paginated_object_kinds(
    session: AsyncSession = SessionDep,
    params: ObjectKindPaginatedParams = Depends(get_object_kind_paginated_params),
):
    """
    Получить список видов объектов с пагинацией.
    """
    handler = ObjectKindHandler()
    result = await handler.get_paginated(session, params.to_pagination())
    return JSONResponse(content=[obj.model_dump() for obj in result])



@router.get("/{id}", response_model=ObjectKindSchema)
async def get_object_kind(
    session: AsyncSession = SessionDep,
    params: ObjectKindGetParams = Depends(get_object_kind_get_params),
) -> ObjectKindSchema | None:
    """
    Получить вид объекта по ID.
    """
    handler = ObjectKindHandler()
    result = await handler.get(session, params.to_get_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Object kind not found")
    return JSONResponse(content=result.model_dump())



@router.post("/", response_model=ObjectKindSchema, status_code=status.HTTP_201_CREATED)
async def create_object_kind(
    session: AsyncSession = SessionDep,
    params: ObjectKindCreateParams = Depends(get_object_kind_create_params),
) -> ObjectKindSchema:
    """
    Создать новый вид объекта.
    """
    handler = ObjectKindHandler()
    
    # Проверяем существование родительского объекта
    if params.parent_id is not None:
        await validate_parent_exists(params.parent_id, handler, session)
    
    # Проверяем существование типа объекта
    await validate_type_exists(params.type_id, session)
    
    result = await handler.create(session, params.to_create_schema())
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)



@router.put("/{id}", response_model=ObjectKindSchema)
async def update_object_kind(
    session: AsyncSession = SessionDep,
    params: ObjectKindUpdateParams = Depends(get_object_kind_update_params),
) -> ObjectKindSchema | None:
    """
    Обновить вид объекта по ID.
    """
    handler = ObjectKindHandler()
    
    # Проверяем существование обновляемого объекта
    existing = await handler.get(session, params.id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Object kind not found")
    
    # Проверяем существование родительского объекта, если он указан
    if params.parent_id is not None:
        await validate_parent_exists(params.parent_id, handler, session)
    
    # Проверяем существование типа объекта, если он указан
    if params.type_id is not None:
        await validate_type_exists(params.type_id, session)
    
    result = await handler.update(session, params.to_edit_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Object kind not found")
    return JSONResponse(content=result.model_dump())



@router.delete("/{id}", response_model=dict)
async def delete_object_kind(
    session: AsyncSession = SessionDep,
    params: ObjectKindDeleteParams = Depends(get_object_kind_delete_params),
) -> dict:
    """
    Удалить вид объекта по ID.
    """
    handler = ObjectKindHandler()
    deleted = await handler.delete(session, params.to_delete_schema())
    if not deleted:
        raise HTTPException(status_code=404, detail="Object kind not found")
    return JSONResponse(content={"status": "success", "message": "Object kind deleted"})



@router.get("/parent/{parent_id}", response_model=list[ObjectKindSchema])
async def get_object_kinds_by_parent(
    session: AsyncSession = SessionDep,
    params: ObjectKindGetChildrenParams = Depends(get_object_kind_get_children_params),
) -> list[ObjectKindSchema]:
    """
    Получить список дочерних видов объектов по parent_id.
    """
    handler = ObjectKindHandler()
    result = await handler.get_children_by_parent(session, params.parent_id)
    return JSONResponse(content=[obj.model_dump() for obj in result])