import secrets
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates

from app.routes.dependsecies.authentication import auth_required
from app.routes.schemas.limit_offset_url import SLimitOffsetUrl
from app.routes.schemas.urls import SUrlIn, SUrlOut
from app.services.dto.dto import (
    RequestDeleteUrlDto,
    RequestInsertUrlDto,
    RequestLimitOffsetUrlDto,
    RequestUpdateUrlDto,
    ResponseUrlDto,
)
from app.services.url_service import UrlService

url_router = APIRouter(tags=["url"], prefix="/url", route_class=DishkaRoute)


templates = Jinja2Templates(directory="../templates")


@url_router.get(
    "/all", response_model=list[SUrlOut] | None, dependencies=[Depends(auth_required)]
)
async def get_all_user_urls(
    schema: Annotated[SLimitOffsetUrl, Depends()], service: FromDishka[UrlService]
) -> list[ResponseUrlDto] | None:
    return await service.get_all_user_urls(
        RequestLimitOffsetUrlDto(limit=schema.limit, offset=schema.offset)
    )


@url_router.post("/insert", dependencies=[Depends(auth_required)])
async def insert_url(
    schema: SUrlIn, service: FromDishka[UrlService]
) -> ResponseUrlDto | None:
    return await service.insert_url(RequestInsertUrlDto(url=schema.url))


@url_router.patch("/change", dependencies=[Depends(auth_required)])
async def change_url(
    url_id: int, service: FromDishka[UrlService]
) -> ResponseUrlDto | None:
    return await service.generate_new_short_url(RequestUpdateUrlDto(url_id))


@url_router.delete("/delete", dependencies=[Depends(auth_required)])
async def delete_url(
    url_id: int, service: FromDishka[UrlService]
) -> ResponseUrlDto | None:
    return await service.delete_url(RequestDeleteUrlDto(url_id))


@url_router.get("/test")
async def test_url() -> str:
    return secrets.choice(["test", "test2", "test3"])
