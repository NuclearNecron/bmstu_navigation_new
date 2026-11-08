from fastapi import Query
from pydantic import BaseModel


class NavigationGetParams(BaseModel):
    """Параметры для построения маршрута между двумя узлами."""

    start_node: int 
    target_node: int 


def get_navigation_params(
    start_node: int = Query(..., description="Идентификатор начального узла", ge=1),
    target_node: int = Query(..., description="Идентификатор целевого узла", ge=1),
) -> NavigationGetParams:
    """Зависимость для получения параметров построения маршрута."""
    return NavigationGetParams(start_node=start_node, target_node=target_node)
