from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.handlers.object_handler import ObjectHandler
from app.handlers.object_type_handler import ObjectTypeHandler
from app.handlers.object_kind_handler import ObjectKindHandler
from app.params.object_params import (
    ObjectCreateParams,
    ObjectDeleteParams,
    ObjectGetAllParams,
    ObjectGetChildrenParams,
    ObjectGetParams,
    ObjectPaginatedParams,
    ObjectUpdateParams,
    get_object_create_params,
    get_object_delete_params,
    get_object_get_all_params,
    get_object_get_children_params,
    get_object_get_params,
    get_object_paginated_params,
    get_object_update_params,
)
from app.schemas.object_models_schemas import (
    NodeTypeCreateParams,
    ObjectSchema,
    ObjectMapperSchema,
)
from app.base.base_schemas import GetSchema

router = APIRouter(
    prefix="/objects",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Depends(get_session)


async def validate_parent_exists(
    parent_id: int, handler: ObjectHandler, session: AsyncSession
):
    """Проверяет существование родительского объекта. Если parent_id is None, возвращает True."""
    if parent_id is None:
        return True

    parent = await handler.get(session, GetSchema(id=parent_id))
    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Parent object with id {parent_id} not found",
        )
    return True



async def validate_kind_exists(kind_id: int, session: AsyncSession):
    """Проверяет существование вида объекта. Если kind_id is None, возвращает True."""
    if kind_id is None:
        return True

    handler = ObjectKindHandler()
    obj_kind = await handler.get(session, GetSchema(id=kind_id))
    if obj_kind is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Object kind with id {kind_id} not found",
        )
    return True


@router.get("/", response_model=list[ObjectSchema])
async def get_all_objects(
    session: AsyncSession = SessionDep,
    params: ObjectGetAllParams = Depends(get_object_get_all_params),
):
    """
    Получить список всех объектов.
    """
    handler = ObjectHandler()
    result = await handler.get_all(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/mapped", response_model=list[ObjectMapperSchema])
async def get_all_objects(
    session: AsyncSession = SessionDep,
    params: ObjectGetAllParams = Depends(get_object_get_all_params),
):
    handler = ObjectHandler()
    result = await handler.get_all_for_mapper(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/page", response_model=list[ObjectSchema])
async def get_paginated_objects(
    session: AsyncSession = SessionDep,
    params: ObjectPaginatedParams = Depends(get_object_paginated_params),
):
    """
    Получить список объектов с пагинацией.
    """
    handler = ObjectHandler()
    result = await handler.get_paginated(session, params.to_pagination())
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/{id}", response_model=ObjectSchema)
async def get_object(
    session: AsyncSession = SessionDep,
    params: ObjectGetParams = Depends(get_object_get_params),
) -> ObjectSchema | None:
    """
    Получить объект по ID.
    """
    handler = ObjectHandler()
    result = await handler.get(session, params.to_get_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Object not found")
    return JSONResponse(content=result.model_dump())


@router.post("/", response_model=ObjectSchema, status_code=status.HTTP_201_CREATED)
async def create_object(
    request: Request,
    session: AsyncSession = SessionDep,
    params: ObjectCreateParams = Depends(get_object_create_params),
) -> ObjectSchema:
    """
    Создать новый объект.
    """
    handler = ObjectHandler()

    # Проверяем существование родительского объекта
    await validate_parent_exists(params.parent_id, handler, session)



    # Проверяем существование вида объекта
    await validate_kind_exists(params.kind_id, session)

    result = await handler.create(session, params.to_create_schema())

    node_type_schema = await handler.get_parent_chain(session, result.id)
    
    await request.app.state.kafka_connection.send_message(
        message={"event": "OBJECT_CREATE", "message": node_type_schema.model_dump()}
    )
    return JSONResponse(
        content=result.model_dump(), status_code=status.HTTP_201_CREATED
    )


@router.put("/{id}", response_model=ObjectSchema)
async def update_object(
    session: AsyncSession = SessionDep,
    params: ObjectUpdateParams = Depends(get_object_update_params),
) -> ObjectSchema | None:
    """
    Обновить объект по ID.
    """
    handler = ObjectHandler()

    # Проверяем существование обновляемого объекта
    existing = await handler.get(session, params.id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Object not found")

    # Проверяем существование родительского объекта, если он указан
    if params.parent_id is not None:
        await validate_parent_exists(params.parent_id, handler, session)


    # Проверяем существование вида объекта, если он указан
    if params.kind_id is not None:
        await validate_kind_exists(params.kind_id, session)

    result = await handler.update(session, params.to_edit_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Object not found")
    return JSONResponse(content=result.model_dump())


@router.delete("/{id}", response_model=dict)
async def delete_object(
    request: Request,
    session: AsyncSession = SessionDep,
    params: ObjectDeleteParams = Depends(get_object_delete_params),
) -> dict:
    """
    Удалить объект по ID.
    """
    handler = ObjectHandler()
    deleted = await handler.delete(session, params.to_delete_schema())
    if not deleted:
        raise HTTPException(status_code=404, detail="Object not found")
    else:
        await request.app.state.kafka_connection.send_message(
            message={"event": "OBJECT_DELETE", "message": params.id}
        )
    return JSONResponse(content={"status": "success", "message": "Object deleted"})


@router.get("/parent/{parent_id}", response_model=list[ObjectSchema])
async def get_objects_by_parent(
    session: AsyncSession = SessionDep,
    params: ObjectGetChildrenParams = Depends(get_object_get_children_params),
) -> list[ObjectSchema]:
    """
    Получить список дочерних объектов по parent_id.
    """
    handler = ObjectHandler()
    result = await handler.get_children_by_parent(session, params.parent_id)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/parent-chain/{id}", response_model=NodeTypeCreateParams)
async def get_parent_chain(
    id: int,
    session: AsyncSession = SessionDep,
) -> NodeTypeCreateParams:
    """
    Получить цепочку родителей объекта.
    """
    handler = ObjectHandler()
    result = await handler.get_parent_chain(session, id)
    return JSONResponse(content=result.model_dump())
