from app.handler.sync_handler import SyncHandler
from app.schemas.nodetype_schemas import (
    NodeTypeCreateParams,
    NodeTypeDeleteParams,
)
import os
from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()
SYNC_HOSTS = os.getenv("SYNC_HOSTS").split(",")

async def create_node_type(params: dict):
    endpoint = "/sync/node-type"
    data = NodeTypeCreateParams(**params)
    for host in SYNC_HOSTS:
        async with AsyncClient() as client:
            url = f"{host.rstrip('/')}{endpoint}"
            response = await client.post(url, json=data.model_dump())
            print(response)
    return None


async def delete_node_type(params: dict):
    data = NodeTypeDeleteParams(**params)
    endpoint =f"/sync/node-type/{params.id}"
    for host in SYNC_HOSTS:
        async with AsyncClient() as client:
            url = f"{host.rstrip('/')}{endpoint}"
            response = await client.delete(url, json=data.model_dump())
            print(response)
    return None
