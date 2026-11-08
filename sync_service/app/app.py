from contextlib import asynccontextmanager
import asyncio

from app.kafka.consumer import KafkaConsumer, consume_messages
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.sleep(20)


    kafka_consumer = KafkaConsumer()
    app.state.kafka_consumer = kafka_consumer
    await app.state.kafka_consumer.start()
    
    # Запускаем consume в фоне
    consume_task = asyncio.create_task(kafka_consumer.consume())
    app.state.consume_task = consume_task

    try:
        yield
    finally:
        consume_task.cancel()
        try:
            await consume_task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="sync service", version="1", lifespan=lifespan)
