from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.routes.schemas.user import SUserIn, SUserOut
from app.services.auth_service import AuthService
from app.services.dto.dto import RequestUserDto

auth_route = APIRouter(tags=["auth"], prefix="/auth", route_class=DishkaRoute)


@auth_route.post("/signup", response_model=SUserOut)
async def signup_user(schema: SUserIn, service: FromDishka[AuthService]) -> dict | None:
    res = await service.create_user(
        RequestUserDto(username=schema.username, password=schema.password)
    )
    if res == "Ok":
        return {"username": schema.username, "urls": None}
    return None
