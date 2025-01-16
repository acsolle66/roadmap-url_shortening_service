from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from ..settings import MONGO_DB, MONGO_URI
from ..shorten.models import URLMap


async def database_init() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(MONGO_URI, server_api=ServerApi("1"))
    models = [URLMap]
    await init_beanie(client[MONGO_DB], document_models=models)
    return client
