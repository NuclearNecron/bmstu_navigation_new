from app.schemas.node_schemas import (
    NodeCreateParams,
    NodeUpdateParams,
    NodeDeleteParams,
)
import os
from httpx import AsyncClient

async def create_node(params: dict):
    endpoint = "/sync/node"
    data = NodeCreateParams(**params)

    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        response = await client.post(url, json=data.model_dump())
        response.raise_for_status()
    return None


async def update_node(params: dict):
    data = NodeUpdateParams(**params)
    endpoint = f"/sync/node/{data.id}"
    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        response = await client.put(url, json=data.model_dump())
        response.raise_for_status()
    return None



async def delete_node(params: dict):
    data = NodeDeleteParams(**params)
    endpoint = f"/sync/node/{data.id}"
    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        response = await client.delete(url, json=data.model_dump())
        response.raise_for_status()
    return None