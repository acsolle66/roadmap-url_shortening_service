from fastapi import APIRouter

# from database.db import client

health = APIRouter(prefix="/health")


@health.get("/ping")
def ping():
    # database = client.short_urls
    # collection = database.url_maps

    # data = {"url": {"short": "url", "long": "url"}}
    # post_id = collection.insert_one(data).inserted_id

    return {"msg": "post_id"}
