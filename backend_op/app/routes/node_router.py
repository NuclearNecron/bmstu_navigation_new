from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.handlers.node_handler import NodeHandler
from app.handlers.object_handler import ObjectHandler
from app.handlers.node_type_handler import NodeTypeHandler
from app.params.node_params import (
    NodeCreateParams,
    NodeDeleteParams,
    NodeGetAllParams,
    NodeGetParams,
    NodePaginatedParams,
    NodeUpdateParams,
    get_node_create_params,
    get_node_delete_params,
    get_node_get_all_params,
    get_node_get_params,
    get_node_paginated_params,
    get_node_update_params,
)
from app.schemas.graph_models_schemas import NodeSchema,NodeMapperSchema

router = APIRouter(
    prefix="/nodes",
    tags=["nodes"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Depends(get_session)


async def validate_parent_exists(parent_id: int, handler: NodeHandler, session: AsyncSession):
    """Проверяет существование родительского узла. Если parent_id is None, возвращает True."""
    if parent_id is None:
        return True
    
    parent = await handler.get(session, parent_id)
    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Parent node with id {parent_id} not found"
        )
    return True

async def validate_object_exists(object_id: int, session: AsyncSession):
    """Проверяет существование объекта. Если object_id is None, возвращает True."""
    if object_id is None:
        return True
        
    handler = ObjectHandler()
    obj = await handler.get(session, object_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Object with id {object_id} not found"
        )
    return True

async def validate_type_exists(type_id: int, session: AsyncSession):
    """Проверяет существование типа узла. Если type_id is None, возвращает True."""
    if type_id is None:
        return True
        
    handler = NodeTypeHandler()
    obj_type = await handler.get(session, type_id)
    if obj_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Node type with id {type_id} not found"
        )
    return True


@router.get("/", response_model=list[NodeSchema])
async def get_all_nodes(
    session: AsyncSession = SessionDep,
    params: NodeGetAllParams = Depends(get_node_get_all_params),
):
    """
    Получить список всех узлов.
    """
    handler = NodeHandler()
    result = await handler.get_all(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])

@router.get("/mapped", response_model=list[NodeMapperSchema])
async def get_all_nodes(
    session: AsyncSession = SessionDep,
    params: NodeGetAllParams = Depends(get_node_get_all_params),
):
    """
    Получить список всех узлов.
    """
    handler = NodeHandler()
    result = await handler.get_all_mapped(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/page", response_model=list[NodeSchema])
async def get_paginated_nodes(
    session: AsyncSession = SessionDep,
    params: NodePaginatedParams = Depends(get_node_paginated_params),
):
    """
    Получить список узлов с пагинацией.
    """
    handler = NodeHandler()
    result = await handler.get_paginated(session, params.to_pagination())
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/{id}", response_model=NodeSchema)
async def get_node(
    session: AsyncSession = SessionDep,
    params: NodeGetParams = Depends(get_node_get_params),
) -> NodeSchema | None:
    """
    Получить узел по ID.
    """
    handler = NodeHandler()
    result = await handler.get(session, params.to_get_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return JSONResponse(content=result.model_dump())


@router.post("/", response_model=NodeSchema, status_code=status.HTTP_201_CREATED)
async def create_node(
    session: AsyncSession = SessionDep,
    params: NodeCreateParams = Depends(get_node_create_params),
) -> NodeSchema:
    """
    Создать новый узел.
    """
    handler = NodeHandler()
    
    # Проверяем существование родительского узла
    await validate_parent_exists(params.parent_id, handler, session)
    
    # Проверяем существование объекта
    await validate_object_exists(params.object_id, session)
    
    # Проверяем существование типа узла
    await validate_type_exists(params.type_id, session)
    
    result = await handler.create(session, params.to_create_schema())
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)


@router.put("/{id}", response_model=NodeSchema)
async def update_node(
    session: AsyncSession = SessionDep,
    params: NodeUpdateParams = Depends(get_node_update_params),
) -> NodeSchema | None:
    """
    Обновить узел по ID.
    """
    handler = NodeHandler()
    
    # Проверяем существование обновляемого объекта
    existing = await handler.get(session, params.id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Проверяем существование родительского узла, если он указан
    if params.parent_id is not None:
        await validate_parent_exists(params.parent_id, handler, session)
    
    # Проверяем существование объекта, если он указан
    if params.object_id is not None:
        await validate_object_exists(params.object_id, session)
    
    # Проверяем существование типа узла, если он указан
    if params.type_id is not None:
        await validate_type_exists(params.type_id, session)
    
    result = await handler.update(session, params.to_edit_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return JSONResponse(content=result.model_dump())


@router.delete("/{id}", response_model=dict)
async def delete_node(
    session: AsyncSession = SessionDep,
    params: NodeDeleteParams = Depends(get_node_delete_params),
) -> dict:
    """
    Удалить узел по ID.
    """
    handler = NodeHandler()
    deleted = await handler.delete(session, params.to_delete_schema())
    if not deleted:
        raise HTTPException(status_code=404, detail="Node not found")
    return JSONResponse(content={"status": "success", "message": "Node deleted"})