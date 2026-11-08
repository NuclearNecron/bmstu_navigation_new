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
        enable_auto_commit: bool = False,
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
                group_id="BMSTU",
                # auto_commit_interval_ms=self.auto_commit_interval_ms,
                # value_deserializer=lambda v: json.loads(v.decode("utf-8")),
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
        try:
            while True:
                message = await self.consumer.getone()
                log.info(
                    "Received Kafka message topic=%s partition=%s offset=%s",
                    message.topic,
                    message.partition,
                    message.offset,
                )
                await handle_message(message.value.decode("utf-8"))
                await self.consumer.commit()
        finally:
            await self.stop()

async def consume_messages():
    # consumer = AIOKafkaConsumer(
    #     os.getenv("KAFKA_TOPIC", "nav-updates"),
    #     bootstrap_servers=os.getenv(
    #         "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
    #     ),
    #     group_id="bankrupt_companies_group",
    #     auto_offset_reset="earliest",
    # )
    pass