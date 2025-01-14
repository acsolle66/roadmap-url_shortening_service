from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from settings import TEMPLATE_ROOT, STATIC_ROOT

templates = Jinja2Templates(directory=TEMPLATE_ROOT)

pages = APIRouter()
pages.mount("/static", StaticFiles(directory=STATIC_ROOT), name="static")


@pages.get("/", response_class=HTMLResponse)
def home(request: Request):
    ctx = {"short_url": "short_url"}
    return templates.TemplateResponse(request=request, name="home.html", context=ctx)


@pages.get("/{short_url}", response_class=RedirectResponse)
def resolve_short_url(request: Request, short_url: str):
    ctx = {"short_url": short_url}
    return templates.TemplateResponse(
        request=request, name="home.html", context=ctx, status_code=300
    )
