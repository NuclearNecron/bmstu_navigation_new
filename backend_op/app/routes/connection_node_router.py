from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.handlers.connection_node_handler import ConnectionNodeHandler
from app.handlers.node_handler import NodeHandler
from app.handlers.connection_type_handler import ConnectionTypeHandler
from app.params.connection_node_params import (
    ConnectionNodeCreateParams,
    ConnectionNodeDeleteParams,
    ConnectionNodeGetAllParams,
    ConnectionNodeGetParams,
    ConnectionNodePaginatedParams,
    ConnectionNodeUpdateParams,
    get_connection_node_create_params,
    get_connection_node_delete_params,
    get_connection_node_get_all_params,
    get_connection_node_get_params,
    get_connection_node_paginated_params,
    get_connection_node_update_params,
)
from app.schemas.graph_models_schemas import ConnectionNodeSchema

router = APIRouter(
    prefix="/connection-nodes",
    tags=["connection-nodes"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Depends(get_session)

async def validate_node_exists(node_id: int, session: AsyncSession):
    """Проверяет существование узла."""
    handler = NodeHandler()
    node = await handler.get(session, node_id)
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Node with id {node_id} not found"
        )
    return True

async def validate_connection_type_exists(connection_type_id: int, session: AsyncSession):
    """Проверяет существование типа соединения. Если connection_type_id is None, возвращает True."""
    if connection_type_id is None:
        return True
        
    handler = ConnectionTypeHandler()
    conn_type = await handler.get(session, connection_type_id)
    if conn_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Connection type with id {connection_type_id} not found"
        )
    return True


@router.get("/", response_model=list[ConnectionNodeSchema])
async def get_all_connection_nodes(
    session: AsyncSession = SessionDep,
    params: ConnectionNodeGetAllParams = Depends(get_connection_node_get_all_params),
):
    """
    Получить список всех соединений узлов.
    """
    handler = ConnectionNodeHandler()
    result = await handler.get_all(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])

@router.get("/mapper", response_model=list[ConnectionNodeSchema])
async def get_all_connection_nodes_mapper(
    session: AsyncSession = SessionDep,
    params: ConnectionNodeGetAllParams = Depends(get_connection_node_get_all_params),
):
    """
    Получить список всех соединений узлов.
    """
    handler = ConnectionNodeHandler()
    result = await handler.get_all_connections_mapper(session)
    return JSONResponse(content=result)


@router.get("/page", response_model=list[ConnectionNodeSchema])
async def get_paginated_connection_nodes(
    session: AsyncSession = SessionDep,
    params: ConnectionNodePaginatedParams = Depends(get_connection_node_paginated_params),
):
    """
    Получить список соединений узлов с пагинацией.
    """
    handler = ConnectionNodeHandler()
    result = await handler.get_paginated(session, params.to_pagination())
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/{id}", response_model=ConnectionNodeSchema)
async def get_connection_node(
    session: AsyncSession = SessionDep,
    params: ConnectionNodeGetParams = Depends(get_connection_node_get_params),
) -> ConnectionNodeSchema | None:
    """
    Получить соединение узлов по ID.
    """
    handler = ConnectionNodeHandler()
    result = await handler.get(session, params.to_get_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Connection node not found")
    return JSONResponse(content=result.model_dump())


@router.post("/", response_model=ConnectionNodeSchema, status_code=status.HTTP_201_CREATED)
async def create_connection_node(
    session: AsyncSession = SessionDep,
    params: ConnectionNodeCreateParams = Depends(get_connection_node_create_params),
) -> ConnectionNodeSchema:
    """
    Создать новое соединение узлов.
    """
    handler = ConnectionNodeHandler()
    
    # Проверяем существование первого узла
    await validate_node_exists(params.node_id1, session)
    
    # Проверяем существование второго узла
    await validate_node_exists(params.node_id2, session)
    
    # Проверяем существование типа соединения
    await validate_connection_type_exists(params.connection_type_id, session)
    
    result = await handler.create(session, params.to_create_schema())
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)


@router.put("/{id}", response_model=ConnectionNodeSchema)
async def update_connection_node(
    session: AsyncSession = SessionDep,
    params: ConnectionNodeUpdateParams = Depends(get_connection_node_update_params),
) -> ConnectionNodeSchema | None:
    """
    Обновить соединение узлов по ID.
    """
    handler = ConnectionNodeHandler()
    
    # Проверяем существование обновляемого объекта
    existing = await handler.get(session, params.id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Connection node not found")
    
    # Проверяем существование первого узла, если он указан
    if params.node_id1 is not None:
        await validate_node_exists(params.node_id1, session)
    
    # Проверяем существование второго узла, если он указан
    if params.node_id2 is not None:
        await validate_node_exists(params.node_id2, session)
    
    # Проверяем существование типа соединения, если он указан
    if params.connection_type_id is not None:
        await validate_connection_type_exists(params.connection_type_id, session)
    
    result = await handler.update(session, params.to_edit_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Connection node not found")
    return JSONResponse(content=result.model_dump())



@router.delete("/{id}", response_model=dict)
async def delete_connection_node(
    session: AsyncSession = SessionDep,
    params: ConnectionNodeDeleteParams = Depends(get_connection_node_delete_params),
) -> dict:
    """
    Удалить соединение узлов по ID.
    """
    handler = ConnectionNodeHandler()
    deleted = await handler.delete(session, params.to_delete_schema())
    if not deleted:
        raise HTTPException(status_code=404, detail="Connection node not found")
    return JSONResponse(content={"status": "success", "message": "Connection node deleted"})