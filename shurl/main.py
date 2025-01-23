from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from .auth.models import User
from .auth.routers import auth
from .database.db import database_init
from .health.router import health_router
from .pages.router import pages
from .settings import get_db_config, logger
from .shorten.models import URLMap
from .shorten.routers import shorten

models = [User, URLMap]


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.db_config = get_db_config()
    app.db_client = await database_init(app.db_config, models)
    try:
        ping = await app.db_client.admin.command("ping")
        if ping["ok"] != 1:
            raise Exception("Problem connecting to MongoDB cluster.")
        else:
            logger.info("Connected to MongoDB client.")
    except Exception as e:
        logger.error(e)
    yield
    app.db_client.close()
    logger.info("MongoDB client closed")


api = APIRouter(prefix="/api")
api.include_router(router=health_router)
api.include_router(router=shorten)
api.include_router(router=auth)

app = FastAPI(lifespan=lifespan)
app.include_router(router=api)
app.include_router(router=pages, include_in_schema=False)
