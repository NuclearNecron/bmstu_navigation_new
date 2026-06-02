from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from fastapi import Request
from app.params.sync_params import (
    NodeTypeCreateParams,
    NodeTypeUpdateParams,
    NodeTypeDeleteParams,
    NodeCreateParams,
    NodeUpdateParams,
    NodeDeleteParams,
    ConnectionCreateParams,
    ConnectionUpdateParams,
    ConnectionDeleteParams,
    get_node_type_create_params,
    get_node_type_update_params,
    get_node_type_delete_params,
    get_node_create_params,
    get_node_update_params,
    get_node_delete_params,
    get_connection_create_params,
    get_connection_update_params,
    get_connection_delete_params
)

router = APIRouter(
    prefix="/sync",
    tags=["synchronization"],
    responses={404: {"description": "Not found"}},
)


@router.post("/node-type", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_node_type(request: Request, 
    params: NodeTypeCreateParams = Depends(get_node_type_create_params)
):
    """Создать новый тип узла. Эндпоинт ожидает, пока карта станет доступной (working=True), прежде чем выполнить операцию."""
    try:
        await request.app.state.synchronizer.execute_async(request.app.state.map.add_type, params.id, params.to_create_schema())
        return JSONResponse(
            content={"status": "success", "message": "Node type created", "id": params.id},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/node-type/{id}", response_model=dict)
async def update_node_type(request: Request, 
    params: NodeTypeUpdateParams = Depends(get_node_type_update_params)
):
    """Обновить существующий тип узла. Эндпоинт ожидает, пока карта станет доступной (working=True), прежде чем выполнить операцию."""
    try:
        await request.app.state.synchronizer.execute_async(request.app.state.map.change_type, params.to_update_schema())
        return JSONResponse(
            content={"status": "success", "message": "Node type updated", "id": params.id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/node-type/{id}", response_model=dict)
async def delete_node_type(request: Request, 
    params: NodeTypeDeleteParams = Depends(get_node_type_delete_params)
):
    """Удалить тип узла. Эндпоинт ожидает, пока карта станет доступной (working=True), прежде чем выполнить операцию."""
    try:
        await request.app.state.synchronizer.execute_async(request.app.state.map.delete_type, params.id)
        return JSONResponse(
            content={"status": "success", "message": "Node type deleted", "id": params.id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/node", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_node(request: Request, 
    params: NodeCreateParams = Depends(get_node_create_params)
):
    """Создать новый узел. Эндпоинт ожидает, пока карта станет доступной (working=True), прежде чем выполнить операцию."""
    try:
        await request.app.state.synchronizer.execute_async(request.app.state.map.add_node, params.to_create_schema())
        return JSONResponse(
            content={"status": "success", "message": "Node created", "id": params.id},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/node/{id}", response_model=dict)
async def update_node(request: Request, 
    params: NodeUpdateParams = Depends(get_node_update_params)
):
    """Обновить существующий узел. Эндпоинт ожидает, пока карта станет доступной (working=True), прежде чем выполнить операцию."""
    try:
        await request.app.state.synchronizer.execute_async(request.app.state.map.change_node, params.to_update_schema())
        return JSONResponse(
            content={"status": "success", "message": "Node updated", "id": params.id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/node/{id}", response_model=dict)
async def delete_node(request: Request, 
    params: NodeDeleteParams = Depends(get_node_delete_params)
):
    """Удалить узел. Эндпоинт ожидает, пока карта станет доступной (working=True), прежде чем выполнить операцию."""
    try:
        await request.app.state.synchronizer.execute_async(request.app.state.map.delete_node, params.id)
        return JSONResponse(
            content={"status": "success", "message": "Node deleted", "id": params.id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/connection", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_connection(request: Request, 
    params: ConnectionCreateParams = Depends(get_connection_create_params)
):
    """Создать новую связь. Эндпоинт ожидает, пока карта станет доступной (working=True), прежде чем выполнить операцию."""
    try:
        await request.app.state.synchronizer.execute_async(request.app.state.map.add_conn, params.to_create_schema())
        return JSONResponse(
            content={"status": "success", "message": "Connection created", "id": params.id},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/connection/{id}", response_model=dict)
async def update_connection(request: Request, 
    params: ConnectionUpdateParams = Depends(get_connection_update_params)
):
    """Обновить существующую связь. Эндпоинт ожидает, пока карта станет доступной (working=True), прежде чем выполнить операцию."""
    try:
        await request.app.state.synchronizer.execute_async(request.app.state.map.change_conn, params.to_update_schema())
        return JSONResponse(
            content={"status": "success", "message": "Connection updated", "id": params.id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/connection/{id}", response_model=dict)
async def delete_connection(request: Request, 
    params: ConnectionDeleteParams = Depends(get_connection_delete_params)
):
    """Удалить связь. Эндпоинт ожидает, пока карта станет доступной (working=True), прежде чем выполнить операцию."""
    try:
        await request.app.state.synchronizer.execute_async(request.app.state.map.delete_conn, params.id)
        return JSONResponse(
            content={"status": "success", "message": "Connection deleted", "id": params.id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))