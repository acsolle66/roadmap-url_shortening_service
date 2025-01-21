from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from ..settings import logger
from .models import URLMap
from .schemas import (URLMapCreate, URLMapResponse, URLMapResponseWithStats,
                      URLMapUpdate)

shorten = APIRouter(prefix="/shorten", tags=["Shorten"])


@shorten.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=URLMapResponse,
)
async def insert_url_map(url_map_create: URLMapCreate):
    short_url = URLMap(url=url_map_create.url)
    try:
        await URLMap.insert_one(short_url)
        await short_url.sync()
        return short_url
    except DuplicateKeyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Duplicated keys")


@shorten.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_url_maps():
    url_maps = []
    async for result in URLMap.find_all():
        url_maps.append(URLMapResponse(**result.model_dump()))
    return url_maps


@shorten.get(
    "/{short_code}",
    status_code=status.HTTP_200_OK,
    responses={404: {}},
    response_model=URLMapResponse,
)
async def get_url_map(short_code: str):
    url_map = await URLMap.find_one(URLMap.short_code == short_code)
    if url_map is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return url_map


@shorten.put(
    "/{short_code}",
    status_code=status.HTTP_200_OK,
    responses={404: {}},
    response_model=URLMapResponse,
)
async def update_url_map(short_code: str, url_map_create: URLMapUpdate):
    url_map = await get_url_map(short_code)
    url_map.url = url_map_create.url
    return await url_map.replace()


@shorten.put(
    "/{short_code}/increase",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {}},
)
async def update_url_map(short_code: str):
    url_map = await get_url_map(short_code)
    url_map.access_count += 1
    await url_map.replace()
    return


@shorten.delete(
    "/{short_code}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {}},
)
async def delete_url_map(short_code: str):
    url_map = await get_url_map(short_code)
    await url_map.delete()
    return


@shorten.get(
    "/{short_code}/stats",
    status_code=status.HTTP_200_OK,
    responses={404: {}},
    response_model=URLMapResponseWithStats,
)
async def get_url_map_with_stats(short_code: str):
    return await get_url_map(short_code)
