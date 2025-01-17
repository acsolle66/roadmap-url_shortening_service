from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from ..settings import DBConfig


async def database_init(
    db_config: DBConfig,
    models: list[Document],
) -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(db_config.MONGO_URI, server_api=ServerApi("1"))
    await init_beanie(client[db_config.MONGO_DB], document_models=models)
    return client
