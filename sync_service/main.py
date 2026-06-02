import asyncio
import logging
import os

from dotenv import load_dotenv

from app.kafka.consumer import KafkaConsumer

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)


async def main():
    """Основная функция запуска Kafka consumer."""
    # Получение настроек из переменных окружения
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    group_id = os.getenv("KAFKA_GROUP_ID", "nav-consumer")
    topic = os.getenv("KAFKA_TOPIC", "nav-updates")

    log.info(f"Starting sync service with Kafka bootstrap servers: {bootstrap_servers}")
    log.info(f"Kafka group_id: {group_id}, topic: {topic}")

    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
    )

    try:
        await consumer.consume()
    except KeyboardInterrupt:
        log.info("Shutting down consumer...")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
