from fastapi import APIRouter, Request

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("/ping")
async def ping(request: Request):
    return {"response": "pong"}
