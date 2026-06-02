from app.schemas.node_schemas import (
    NodeCreateParams,
    NodeUpdateParams,
    NodeDeleteParams,
)
import os
from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()
SYNC_HOSTS = os.getenv("SYNC_HOSTS").split(",")

async def create_node(params: dict):
    endpoint = "/sync/node"
    data = NodeCreateParams(**params)
    for host in SYNC_HOSTS:
        async with AsyncClient() as client:
            url = f"{host.rstrip('/')}{endpoint}"
            response = await client.post(url, json=data.model_dump())
            print(response)
    return None


async def update_node(params: dict):
    data = NodeUpdateParams(**params)
    endpoint = f"/sync/node/{params.id}"
    for host in SYNC_HOSTS:
        async with AsyncClient() as client:
            url = f"{host.rstrip('/')}{endpoint}"
            response = await client.put(url, json=data.model_dump())
            print(response)
    return None



async def delete_node(params: dict):
    data = NodeDeleteParams(**params)
    endpoint = f"/sync/node/{params.id}"
    for host in SYNC_HOSTS:
        async with AsyncClient() as client:
            url = f"{host.rstrip('/')}{endpoint}"
            response = await client.delete(url, json=data.model_dump())
            print(response)
    return None