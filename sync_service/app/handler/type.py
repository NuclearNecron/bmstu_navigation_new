from app.schemas.nodetype_schemas import (
    NodeTypeCreateParams,
    NodeTypeDeleteParams,
)
import os
from httpx import AsyncClient
from dotenv import load_dotenv

async def create_node_type(params: dict):
    endpoint = "/sync/node-type"
    data = NodeTypeCreateParams(**params)
    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        print(url)
        response = await client.post(url, json=data.model_dump())
        print(response)
    return None


async def delete_node_type(params: dict):
    data = NodeTypeDeleteParams(**params)
    endpoint =f"/sync/node-type/{params.id}"
    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        print(url)
        response = await client.delete(url, json=data.model_dump())
        print(response)
    return None
