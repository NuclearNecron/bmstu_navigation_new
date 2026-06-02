from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.map.mapper import Map
from app.sync.synchronizer import Synchronizer
from app.routes.sync_router import sync_router
from app.routes.navigation_router import navigation_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    # Инициализация ресурсов при запуске приложения
    app.state.map = Map()
    app.state.synchronizer = Synchronizer()
    await app.state.map.start()  # Запуск и загрузка данных
    
    yield  # Передача управления приложению
    
    # Освобождение ресурсов при завершении приложения
    app.state.map = None

app = FastAPI(title="Navigation Service", lifespan=lifespan)

app.include_router(sync_router)
app.include_router(navigation_router)