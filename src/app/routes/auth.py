import json
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.auth.jwt_processor import JwtTokenProcessor
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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: FromDishka[AuthService],
    response: Response,
    request: Request,
) -> dict[str, str]:
    res = await service.register(
        RequestUserDto(username=form_data.username, password=form_data.password)
    )
    response.headers["HX-Location"] = json.dumps(
        {
            "path": request.url_for("index").path,
        }
    )
    return {"message": res}


@auth_route.post("/login", response_model=SUserOut)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: FromDishka[AuthService],
    response: Response,
    token_processor: FromDishka[JwtTokenProcessor],
    request: Request,
) -> ResponseUserDto:
    user = await service.login(
        RequestUserDto(username=form_data.username, password=form_data.password)
    )
    token = token_processor.generate_token(user.uid)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    response.headers["HX-Location"] = json.dumps(
        {"path": request.url_for("get_all_user_urls").path, "target": "#response-div"}
    )

    return user
