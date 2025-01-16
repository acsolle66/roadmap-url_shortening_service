from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from .database.db import database_init
from .health.router import health_router
from .pages.router import pages
from .settings import logger
from .shorten.routers import shorten


@asynccontextmanager
async def lifespan(app: FastAPI):
    client: AsyncIOMotorClient = await database_init()
    try:
        ping = await client.admin.command("ping")
        if ping["ok"] != 1:
            raise Exception("Problem connecting to MongoDB cluster.")
        else:
            logger.info("Connected to MongoDB client.")
    except Exception as e:
        logger.error(e)
    yield
    client.close()
    logger.info("MongoDB client closed")


api = APIRouter(prefix="/api")
api.include_router(router=health_router)
api.include_router(router=shorten)

app = FastAPI(lifespan=lifespan)
app.include_router(router=api)
app.include_router(router=pages, include_in_schema=False)
