from app.schemas.nodetype_schemas import (
    NodeTypeCreateParams,
    NodeTypeDeleteParams,
)
import os
from httpx import AsyncClient

async def create_node_type(params: dict):
    endpoint = "/sync/node-type"
    data = NodeTypeCreateParams(**params)
    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        response = await client.post(url, json=data.model_dump())
        response.raise_for_status()
    return None


async def delete_node_type(params: dict):
    data = NodeTypeDeleteParams(**params)
    endpoint = f"/sync/node-type/{data.id}"
    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        response = await client.delete(url, json=data.model_dump())
        response.raise_for_status()
    return None
