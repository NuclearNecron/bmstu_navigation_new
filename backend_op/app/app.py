import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from app.database.database import db_engine
from app.kafka.producer import KafkaConnection
from app.routes import main_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler(os.path.join(PROJECT_ROOT, "logs", "app.log")),
        logging.StreamHandler(),
    ],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.sleep(15)


    kafka_conn = KafkaConnection()
    await kafka_conn.start()
    app.state.kafka_connection = kafka_conn

    try:
        yield
    finally:
        await kafka_conn.stop()
        await db_engine.dispose()


app = FastAPI(title="BMSTU Navigation API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутера статики
app.include_router(main_router)

# Раздача статических файлов через FastAPI
STATIC_DIR = Path(__file__).parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static/files", StaticFiles(directory=str(STATIC_DIR)), name="static_files")
