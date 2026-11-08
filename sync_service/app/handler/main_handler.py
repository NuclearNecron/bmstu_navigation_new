import json
import logging

from app.handler.connection import create_connection, delete_connection, update_connection
from app.handler.node import create_node, delete_node, update_node
from app.handler.type import create_node_type, delete_node_type, update_node_type


async def handle_message(message: str):
    message_dict = json.loads(message)

    event = message_dict.get("event")
    data = message_dict.get("message", {})

    log.info("Processing event %s", event)

    match event:
        case "OBJECT_CREATE":
            results = await create_node_type(data)
            log.info("Object map type created: %s", results)

        case "OBJECT_DELETE":
            results = await delete_node_type({"id": data})
            log.info("Object map type deleted: %s", results)

        case "NODE_TYPE_DELETE":
            results = await delete_node_type(data)
            log.info("Node type deleted: %s", results)

        case "NODE_CREATE":
            results = await create_node(data)
            log.info("Node created: %s", results)

        case "NODE_UPDATE":
            results = await update_node(data)
            log.info("Node updated: %s", results)

        case "NODE_DELETE":
            results = await delete_node(data)
            log.info("Node deleted: %s", results)

        case "CONNECTION_CREATE":
            results = await create_connection(data)
            log.info("Connection created: %s", results)

        case "CONNECTION_UPDATE":
            results = await update_connection(data)
            log.info("Connection updated: %s", results)

        case "CONNECTION_DELETE":
            results = await delete_connection(data)
            log.info("Connection deleted: %s", results)

        case _:
            raise ValueError(f"Unknown event type: {event}")
