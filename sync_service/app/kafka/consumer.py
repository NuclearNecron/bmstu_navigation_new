import json
import logging
import os

from aiokafka import AIOKafkaConsumer
from app.handler.main_handler import handle_message

log = logging.getLogger(__name__)


class KafkaConsumer:
    """Kafka consumer с auto_commit."""

    def __init__(
        self,
        bootstrap_servers: str = None,
        auto_offset_reset: str = "earliest",
        enable_auto_commit: bool = True,
        auto_commit_interval_ms: int = 1000,
    ):
        self.bootstrap_servers = bootstrap_servers or os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
        )
        self.auto_offset_reset = auto_offset_reset
        self.enable_auto_commit = enable_auto_commit
        self.auto_commit_interval_ms = auto_commit_interval_ms
        self.consumer: AIOKafkaConsumer | None = None
        self._topic = os.getenv("KAFKA_TOPIC", "nav-updates")

    async def start(self):
        """Запуск Kafka consumer."""
        if self.consumer is None:
            self.consumer = AIOKafkaConsumer(
                self._topic,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset=self.auto_offset_reset,
                enable_auto_commit=self.enable_auto_commit,
                auto_commit_interval_ms=self.auto_commit_interval_ms,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
            await self.consumer.start()
            log.info("Kafka consumer started")

    async def stop(self):
        """Остановка Kafka consumer."""
        if self.consumer:
            await self.consumer.stop()
            self.consumer = None
            log.info("Kafka consumer stopped")

    async def consume(self):

        await self.start()
        try:
            while True:
                try:
                    message = await self.consumer.getone()

                    if message:
                        log.info(f"Received message: {message}")
                        await handle_message(message.value.decode("utf-8"))
                    else:
                        continue
                except Exception as e:
                    log.error(f"Error consuming message: {e}")
                    # В случае ошибки продолжаем попытки получения сообщений
                    continue
        finally:
            await self.stop()
