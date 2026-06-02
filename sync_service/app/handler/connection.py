from app.schemas.connection_schemas import (
    ConnectionCreateParams,
    ConnectionUpdateParams,
    ConnectionDeleteParams,
)


import os
from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()
SYNC_HOSTS = os.getenv("SYNC_HOSTS").split(",")

async def create_connection(params: dict):
    endpoint = "/sync/connection"
    data = ConnectionCreateParams(**params)
    for host in SYNC_HOSTS:
        async with AsyncClient() as client:
            url = f"{host.rstrip('/')}{endpoint}"
            response = await client.post(url, json=data.model_dump())
            print(response)
    return None


async def update_connection(params: dict):
    data = ConnectionUpdateParams(**params)
    endpoint = f"/sync/connection/{data.id}"
    for host in SYNC_HOSTS:
        async with AsyncClient() as client:
            url = f"{host.rstrip('/')}{endpoint}"
            response = await client.put(url, json=data.model_dump())
            print(response)
    return None


async def delete_connection(params: dict):
    data = ConnectionDeleteParams(**params)
    endpoint = f"/sync/connection/{params.id}"
    for host in SYNC_HOSTS:
        async with AsyncClient() as client:
            url = f"{host.rstrip('/')}{endpoint}"
            response = await client.delete(url, json=data.model_dump())
            print(response)
    return None
