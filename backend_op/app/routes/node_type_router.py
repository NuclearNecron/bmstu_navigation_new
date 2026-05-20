from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.handlers.node_type_handler import NodeTypeHandler
from app.params.node_type_params import (
    NodeTypeCreateParams,
    NodeTypeDeleteParams,
    NodeTypeGetAllParams,
    NodeTypeGetParams,
    NodeTypePaginatedParams,
    NodeTypeUpdateParams,
    get_node_type_create_params,
    get_node_type_delete_params,
    get_node_type_get_all_params,
    get_node_type_get_params,
    get_node_type_paginated_params,
    get_node_type_update_params,
)
from app.schemas.graph_models_schemas import NodeTypeSchema

router = APIRouter(
    prefix="/node-types",
    tags=["node-types"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Depends(get_session)


@router.get("/", response_model=list[NodeTypeSchema])
async def get_all_node_types(
    session: AsyncSession = SessionDep,
    params: NodeTypeGetAllParams = Depends(get_node_type_get_all_params),
):
    """
    Получить список всех типов узлов.
    """
    handler = NodeTypeHandler()
    result = await handler.get_all(session)
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/page", response_model=list[NodeTypeSchema])
async def get_paginated_node_types(
    session: AsyncSession = SessionDep,
    params: NodeTypePaginatedParams = Depends(get_node_type_paginated_params),
):
    """
    Получить список типов узлов с пагинацией.
    """
    handler = NodeTypeHandler()
    result = await handler.get_paginated(session, params.to_pagination())
    return JSONResponse(content=[obj.model_dump() for obj in result])


@router.get("/{id}", response_model=NodeTypeSchema)
async def get_node_type(
    session: AsyncSession = SessionDep,
    params: NodeTypeGetParams = Depends(get_node_type_get_params),
) -> NodeTypeSchema | None:
    """
    Получить тип узла по ID.
    """
    handler = NodeTypeHandler()
    result = await handler.get(session, params.to_get_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Node type not found")
    return JSONResponse(content=result.model_dump())


@router.post("/", response_model=NodeTypeSchema, status_code=status.HTTP_201_CREATED)
async def create_node_type(
    session: AsyncSession = SessionDep,
    params: NodeTypeCreateParams = Depends(get_node_type_create_params),
) -> NodeTypeSchema:
    """
    Создать новый тип узла.
    """
    handler = NodeTypeHandler()
    result = await handler.create(session, params.to_create_schema())
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)


@router.put("/{id}", response_model=NodeTypeSchema)
async def update_node_type(
    session: AsyncSession = SessionDep,
    params: NodeTypeUpdateParams = Depends(get_node_type_update_params),
) -> NodeTypeSchema | None:
    """
    Обновить тип узла по ID.
    """
    handler = NodeTypeHandler()
    
    # Проверяем существование обновляемого объекта
    existing = await handler.get(session, params.id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Node type not found")
    
    result = await handler.update(session, params.to_edit_schema())
    if result is None:
        raise HTTPException(status_code=404, detail="Node type not found")
    return JSONResponse(content=result.model_dump())


@router.delete("/{id}", response_model=dict)
async def delete_node_type(
    session: AsyncSession = SessionDep,
    params: NodeTypeDeleteParams = Depends(get_node_type_delete_params),
) -> dict:
    """
    Удалить тип узла по ID.
    """
    handler = NodeTypeHandler()
    deleted = await handler.delete(session, params.to_delete_schema())
    if not deleted:
        raise HTTPException(status_code=404, detail="Node type not found")
    return JSONResponse(content={"status": "success", "message": "Node type deleted"})