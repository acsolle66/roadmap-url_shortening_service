from typing import Annotated
from urllib import response
import httpx
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..settings import STATIC_ROOT, TEMPLATE_ROOT
from ..shorten.routers import get_url_map

templates = Jinja2Templates(directory=TEMPLATE_ROOT)

pages = APIRouter()
pages.mount("/static", StaticFiles(directory=STATIC_ROOT), name="static")


@pages.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={})


@pages.post("/", response_class=HTMLResponse)
def home(request: Request, long_url: Annotated[str, Form()]):
    response = httpx.post("http://127.0.0.1:8000/api/shorten/", json={"url": long_url})
    ctx = {"short_code": response.json()["shortCode"]}
    return templates.TemplateResponse(request=request, name="home.html", context=ctx)


@pages.get("/{short_code}")
def redirect_short_code(request: Request, short_code: str):
    short_url = "http://127.0.0.1:8000/api/shorten/" + short_code
    response = httpx.get(short_url)

    if response.status_code == 404:
        return templates.TemplateResponse(
            request=request,
            name="not_found.html",
            context={},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    httpx.put(short_url + "/increase")

    headers = {"Cache-Control": "no-store"}
    return RedirectResponse(
        response.json()["url"],
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
        headers=headers,
    )
