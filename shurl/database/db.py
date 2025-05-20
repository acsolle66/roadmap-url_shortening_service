import asyncio

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from ..settings import DBConfig

# https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop


async def database_init(
    db_config: DBConfig,
    models: list[Document],
) -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(db_config.MONGO_URI, server_api=ServerApi("1"))
    client.get_io_loop = asyncio.get_running_loop
    await init_beanie(client[db_config.MONGO_DB], document_models=models)
    return client
