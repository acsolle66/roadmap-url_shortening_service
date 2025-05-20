from typing import Annotated

import httpx
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..settings import STATIC_ROOT, TEMPLATE_ROOT, logger
from ..shorten.routers import get_url_map

templates = Jinja2Templates(directory=TEMPLATE_ROOT)

pages = APIRouter()
#pages.mount("/static", StaticFiles(directory=STATIC_ROOT), name="static")

api_host = "http://127.0.0.1:8000/api"


def set_authentication_header(request: Request):
    headers = {}
    access_token = request.cookies.get("id")
    if access_token is not None:
        headers["Authorization"] = "Bearer " + access_token
    return headers


@pages.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    headers = set_authentication_header(request)
    r = httpx.get(api_host + "/auth/users/me", follow_redirects=True, headers=headers)
    if r.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(
            "http://127.0.0.1:8000/login",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    r = httpx.get(api_host + "/shorten/", follow_redirects=True, headers=headers)
    urls = r.json()
    ctx = {"short_urls": urls}
    return templates.TemplateResponse(request=request, name="home.html", context=ctx)


@pages.post("/", response_class=HTMLResponse)
def add_url(request: Request, url: Annotated[str, Form()]):
    headers = set_authentication_header(request)

    r = httpx.get(api_host + "/auth/users/me", follow_redirects=True, headers=headers)
    if r.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(
            "http://127.0.0.1:8000/login",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    httpx.post(
        api_host + "/shorten",
        json={"url": url},
        follow_redirects=True,
        headers=headers,
    )

    r = httpx.get(api_host + "/shorten/", follow_redirects=True, headers=headers)
    urls = r.json()
    ctx = {"short_urls": urls}
    return templates.TemplateResponse(request=request, name="home.html", context=ctx)


@pages.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})


@pages.post("/login", response_class=HTMLResponse)
async def post_login(request: Request):
    form_data = await request.form()
    username = form_data.__getitem__("username")
    password = form_data.__getitem__("password")
    form = {"username": username, "password": password}
    client = httpx.AsyncClient()
    r = await client.post(api_host + "/auth/token/", follow_redirects=True, data=form)
    if r.status_code == status.HTTP_200_OK:
        access_token = r.json().get("access_token")
        response = RedirectResponse(
            "http://127.0.0.1:8000/",
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )
        response.set_cookie(key="id", value=access_token)
        return response
    return templates.TemplateResponse(request=request, name="login.html", context={})


@pages.get("/{short_code}", response_class=HTMLResponse)
async def redirect_to_url(request: Request, short_code: str):
    client = httpx.AsyncClient()
    r = await client.get(api_host + "/shorten/" + short_code, follow_redirects=True)
    if r.status_code == status.HTTP_200_OK:
        url = r.json().get("url")
        headers = {"Cache-Control": "no-store"}
        r = await client.put(
            api_host + "/shorten/" + short_code + "/increase", follow_redirects=True
        )
        return RedirectResponse(
            url, status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers=headers
        )
    return templates.TemplateResponse(
        request=request,
        name="not_found.html",
        context={},
        status_code=status.HTTP_404_NOT_FOUND,
    )
