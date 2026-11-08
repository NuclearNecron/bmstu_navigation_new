import os
from aiokafka import AIOKafkaProducer
import json


class KafkaConnection:
    _instance = None

    def __new__(cls, bootstrap_servers: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, bootstrap_servers: str = None):
        # Only initialize once
        if not hasattr(self, "initialized"):
            self.bootstrap_servers = bootstrap_servers or os.getenv(
                "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
            )
            self.producer = None
            self.initialized = True
            self.topic = os.getenv("KAFKA_TOPIC", "nav-updates")

    async def start(self):
        """Initialize the Kafka producer."""
        if self.producer is None:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,   
                max_request_size=52_428_800,
            )
            await self.producer.start()

    async def stop(self):
        """Stop the Kafka producer."""
        if self.producer:
            await self.producer.stop()
            self.producer = None

    async def send_message(self, message: dict):
        """Send a message to Kafka topic."""
        if not self.producer:
            raise RuntimeError("Kafka producer not initialized. Call start() first.")

        try:
            # Convert message to JSON and encode to bytes
            value = json.dumps(message).encode("utf-8")

            await self.producer.send_and_wait(
                topic=self.topic,
                value=value,
            )
        except Exception as e:
            # Log the error and re-raise
            print(f"Error sending message to Kafka: {e}")
            raise

    def is_connected(self) -> bool:
        """Check if producer is connected."""
        return self.producer is not None
