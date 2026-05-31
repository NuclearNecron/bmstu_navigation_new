import asyncio
import logging
import os
from contextlib import asynccontextmanager

from app.database.database import get_session
from app.kafka.producer import KafkaConnection
from app.routes import main_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

    asyncio.sleep(20)

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

app.include_router(main_router)