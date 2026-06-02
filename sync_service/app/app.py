import asyncio
from contextlib import asynccontextmanager

from app.kafka.consumer import KafkaConsumer
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.sleep(20)
    kafka_consumer = KafkaConsumer()
    await kafka_consumer.start()
    app.state.kafka_consumer = kafka_consumer
    yield


app = FastAPI(title="sync service", version="1", lifespan=lifespan)
