import json
import logging

from app.handler.connection import create_connection, delete_connection, update_connection
from app.handler.node import create_node, delete_node, update_node
from app.handler.type import create_node_type, delete_node_type

log = logging.getLogger(__name__)


async def handle_message(message: str):
    message_dict = json.loads(message)

    event = message_dict.get("event")
    data = message_dict.get("data", {})


    log.info(f"Processing event: {event}")

    match event:
        case "OBJECT_CREATE":
            results = await create_node_type(data)
            log.info(f"Node type create results: {results}")

        case "NODE_TYPE_DELETE":
            results = await delete_node_type(data)
            log.info(f"Node type delete results: {results}")

        case "NODE_CREATE":
            results = await create_node(data)
            log.info(f"Node create results: {results}")

        case "NODE_UPDATE":
            results = await update_node(data)
            log.info(f"Node update results: {results}")

        case "NODE_DELETE":
            results = await delete_node(data)
            log.info(f"Node delete results: {results}")

        case "CONNECTION_CREATE":
            results = await create_connection(data)
            log.info(f"Connection create results: {results}")

        case "CONNECTION_UPDATE":
            results = await update_connection(data)
            log.info(f"Connection update results: {results}")

        case "CONNECTION_DELETE":
            results = await delete_connection(data)
            log.info(f"Connection delete results: {results}")

        case _:
            log.warning(f"Unknown event type: {event}")
