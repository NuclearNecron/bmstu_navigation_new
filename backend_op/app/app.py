import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from app.database.database import get_session
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

    session = await anext(get_session())
    app.state.db_session = session

    await asyncio.sleep(5)

    # Initialize Kafka connection (singleton)
    kafka_conn = KafkaConnection()
    await kafka_conn.start()

    # Store in app state for access by routes
    app.state.kafka_connection = kafka_conn

    try:
        yield
    finally:
        # Cleanup on shutdown
        await app.state.kafka_connection.stop()


app = FastAPI(title="BMSTU Navigation API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутера статики
app.include_router(main_router)

# Раздача статических файлов через FastAPI
STATIC_DIR = Path(__file__).parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static/files", StaticFiles(directory=str(STATIC_DIR)), name="static_files")
