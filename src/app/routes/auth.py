from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response
from fastapi.templating import Jinja2Templates

from app.auth.jwt_processor import JwtTokenProcessor
from app.routes.schemas.user import SUserIn, SUserOut
from app.services.auth_service import AuthService
from app.services.dto.dto import (
    RequestUserDto,
    ResponseUserDto,
)

auth_route = APIRouter(tags=["auth"], prefix="/auth", route_class=DishkaRoute)

templates = Jinja2Templates(directory="../templates")

@auth_route.post("/signup")
async def signup_user(
    schema: SUserIn, service: FromDishka[AuthService]
) -> dict[str, str]:
    res = await service.register(
        RequestUserDto(username=schema.username, password=schema.password)
    )
    return {"message": res}


@auth_route.post("/login", response_model=SUserOut)
async def login_user(
    schema: SUserIn,
    service: FromDishka[AuthService],
    response: Response,
    token_processor: FromDishka[JwtTokenProcessor],
) -> ResponseUserDto:
    user = await service.login(
        RequestUserDto(username=schema.username, password=schema.password)
    )
    token = token_processor.generate_token(user.uid)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)

    return user
