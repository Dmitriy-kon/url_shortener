from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Response
from fastapi.templating import Jinja2Templates

from app.auth.jwt_processor import JwtTokenProcessor
from app.routes.schemas.oauth2_password_form import OAuth2PasswordForm
from app.routes.schemas.user import SUserOut
from app.services.auth_service import AuthService
from app.services.dto.dto import (
    RequestUserDto,
    ResponseUserDto,
)

auth_route = APIRouter(tags=["auth"], prefix="/auth", route_class=DishkaRoute)

templates = Jinja2Templates(directory="src/app/templates")


@auth_route.post("/signup")
async def signup_user(
    form_data: Annotated[OAuth2PasswordForm, Depends()],
    service: FromDishka[AuthService],
) -> dict[str, str]:
    await service.register(
        RequestUserDto(username=form_data.username, password=form_data.password)
    )

    return {"message": "user created"}


@auth_route.post("/login", response_model=SUserOut)
async def login_user(
    form_data: Annotated[OAuth2PasswordForm, Depends()],
    service: FromDishka[AuthService],
    response: Response,
    token_processor: FromDishka[JwtTokenProcessor],
) -> ResponseUserDto:
    user = await service.login(
        RequestUserDto(username=form_data.username, password=form_data.password)
    )
    token = token_processor.generate_token(user.uid)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)

    return user
