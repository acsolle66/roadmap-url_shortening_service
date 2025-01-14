from fastapi import APIRouter
from .health.router import health

api_v1 = APIRouter(tags=["Health"])

api_v1.include_router(router=health)
