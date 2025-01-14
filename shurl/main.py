from fastapi import FastAPI
from api.router import api_v1
from pages.router import pages

app = FastAPI()
app.include_router(router=api_v1, prefix="/api/v1")
app.include_router(router=pages)
