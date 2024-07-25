from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.routes.schemas.user import SUserIn, SUserOut
from app.services.auth_service import AuthService
from app.services.dto.dto import RequestUserDto

auth_route = APIRouter(tags=["auth"], prefix="/auth", route_class=DishkaRoute)


@auth_route.post("/signup")
async def signup_user(
    schema: SUserIn, service: FromDishka[AuthService]
) -> dict[str, str]:
    res = await service.register(
        RequestUserDto(username=schema.username, password=schema.password)
    )
    return {"message": res}


@auth_route.post("/login")
async def login_user(
    schema: SUserIn, service: FromDishka[AuthService]
) -> dict[str, str]:
    res = await service.login(
        RequestUserDto(username=schema.username, password=schema.password)
    )
    return {"message": "ok", "id": str(res.uid)}
