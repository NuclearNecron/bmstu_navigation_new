from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.params.navigation_params import NavigationGetParams, get_navigation_params

router = APIRouter(
    prefix="/navigation",
    tags=["navigation"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=dict)
async def get_navigation(
    request: Request, params: NavigationGetParams = Depends(get_navigation_params)
):
    """
    Построить маршрут между двумя узлами.
    """
    map_instance = request.app.state.map

    # Проверяем существование узлов
    if params.start_node not in map_instance.nodes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with id {params.start_node} not found",
        )

    if params.target_node not in map_instance.nodes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with id {params.target_node} not found",
        )

    # Проверяем, что карта готова к работе
    if not map_instance.working:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Map is not ready. Still loading data.",
        )

    # Строим маршрут
    try:
        result = await map_instance.navigate_main(params.start_node, params.target_node)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot build route between nodes",
            )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
