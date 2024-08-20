from typing import Annotated, cast

from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from app.services.common.exception import UserIsNotAuthorizedError


class Oath2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenurl: str,
        scheme_name: str | None = None,
        scopes: dict[str, str] | None = None,
        *,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password=cast(OAuthFlowPassword, {"tokenUrl": tokenurl, "scopes": scopes})
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization: str | None = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if authorization is None or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return param


oauth2_scheme = Oath2PasswordBearerWithCookie(tokenurl="/auth/login")


async def auth_required(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    if not token:
        raise UserIsNotAuthorizedError("Неверные данные для авторизации")
    request.scope["auth"] = token
