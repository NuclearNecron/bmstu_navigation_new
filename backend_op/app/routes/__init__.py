"""HTTP-эндпоинты (роутеры). Параметры запросов — в app.params."""

from fastapi import APIRouter

from app.routes.object_router import router as object_router
from app.routes.object_type_router import router as object_type_router
from app.routes.object_kind_router import router as object_kind_router
from app.routes.node_router import router as node_router
from app.routes.node_type_router import router as node_type_router
from app.routes.object_state_router import router as object_state_router
from app.routes.connection_type_router import router as connection_type_router
from app.routes.connection_object_router import router as connection_object_router
from app.routes.connection_node_router import router as connection_node_router
from app.routes.static_router import router as static_router

main_router = APIRouter()
main_router.include_router(object_router)
main_router.include_router(object_type_router)
main_router.include_router(object_kind_router)
main_router.include_router(node_router)
main_router.include_router(node_type_router)
main_router.include_router(object_state_router)
main_router.include_router(connection_type_router)
main_router.include_router(connection_object_router)
main_router.include_router(connection_node_router)
main_router.include_router(static_router)

__all__ = ["main_router"]
