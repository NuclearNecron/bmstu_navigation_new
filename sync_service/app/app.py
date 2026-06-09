import asyncio

from contextlib import asynccontextmanager

from app.kafka.consumer import KafkaConsumer, consume_messages
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.sleep(20)
    print("satrtaing")
    # kafka_consumer = KafkaConsumer()
    # app.state.kafka_consumer = kafka_consumer
    # await app.state.kafka_consumer.consume()
    
    # yield
    kafka_consumer = KafkaConsumer()
    app.state.kafka_consumer = kafka_consumer
    await app.state.kafka_consumer.start()
    
    # Запускаем consume в фоне
    consume_task = asyncio.create_task(kafka_consumer.consume())
    app.state.consume_task = consume_task

    yield
    
    await kafka_consumer.stop()


app = FastAPI(title="sync service", version="1", lifespan=lifespan)
