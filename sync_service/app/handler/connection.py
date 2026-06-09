from app.schemas.connection_schemas import (
    ConnectionCreateParams,
    ConnectionUpdateParams,
    ConnectionDeleteParams,
)


import os
from httpx import AsyncClient

async def create_connection(params: dict):
    endpoint = "/sync/connection"
    data = ConnectionCreateParams(**params)
    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        response = await client.post(url, json=data.model_dump())
        print(response)
    return None


async def update_connection(params: dict):
    data = ConnectionUpdateParams(**params)
    endpoint = f"/sync/connection/{data.id}"
    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        response = await client.put(url, json=data.model_dump())
        print(response)
    return None


async def delete_connection(params: dict):
    data = ConnectionDeleteParams(**params)
    endpoint = f"/sync/connection/{params.id}"
    async with AsyncClient() as client:
        url = f"http://{os.getenv("SYNC_HOSTS")}{endpoint}"
        response = await client.delete(url, json=data.model_dump())
        print(response)
    return None
