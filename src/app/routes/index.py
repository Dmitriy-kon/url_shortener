from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.routes.schemas.urls import SUrlInQuery
from app.services.get_short_url import GetUrlFromShortUrl

index_route = APIRouter(tags=["index"], route_class=DishkaRoute)


templates = Jinja2Templates(directory="src/app/templates")


@index_route.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@index_route.get("/t")
async def get_url_from_short(
    schema: Annotated[SUrlInQuery, Depends()],
    get_url_from_short_url: FromDishka[GetUrlFromShortUrl],
    # config: FromDishka[Config],
) -> RedirectResponse:
    res = await get_url_from_short_url(schema.short)
    if not res:
        return RedirectResponse("/")
    return RedirectResponse(res.url)
