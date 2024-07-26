from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from app.routes.dependsecies.authentication import auth_required
from app.routes.schemas.limit_offset_url import SLimitOffsetUrl
from app.routes.schemas.urls import SUrlIn, SUrlOut
from app.services.dto.dto import (
    RequestInsertUrlDto,
    RequestLimitOffsetUrlDto,
    ResponseUrlDto,
)
from app.services.url_service import UrlService

url_router = APIRouter(tags=["url"], prefix="/url", route_class=DishkaRoute)


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
