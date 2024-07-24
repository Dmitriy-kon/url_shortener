from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.routes.schemas.limit_offset_url import SLimitOffsetUrl
from app.routes.schemas.urls import SUrlOut
from app.services.dto.dto import RequestLimitOffsetUrlDto, ResponseUrlDto
from app.services.url_service import UrlService

url_router = APIRouter(tags=["url"], prefix="/url", route_class=DishkaRoute)


@url_router.get("/all", response_model=list[SUrlOut])
async def get_all_user_urls(
    schema: SLimitOffsetUrl, service: FromDishka[UrlService]
) -> list[ResponseUrlDto] | None:
    return await service.get_all_user_urls(
        RequestLimitOffsetUrlDto(
            limit=schema.limit, offset=schema.offset, user_id=schema.user_id
        )
    )
