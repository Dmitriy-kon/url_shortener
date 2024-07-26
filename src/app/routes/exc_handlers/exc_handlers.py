from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler

from app.services.common.exception import (
    UrlAllreadyExistsError,
    UserAlreadyExistsError,
    UserIsNotAuthorizedError,
    UserNotFoundError,
    UserPasswordNotMatchError,
)


async def user_not_found_handler(
    request: Request, exc: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


async def user_is_not_authorized_handler(
    request: Request, exc: UserIsNotAuthorizedError
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"message": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def user_already_exists_handler(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": exc.message},
    )


async def user_password_not_match_handler(
    request: Request, exc: UserPasswordNotMatchError
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"message": exc.message},
    )


async def url_allready_exists_handler(
    request: Request, exc: UrlAllreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": exc.message},
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UserNotFoundError, cast(ExceptionHandler, user_not_found_handler)
    )
    app.add_exception_handler(
        UserAlreadyExistsError, cast(ExceptionHandler, user_already_exists_handler)
    )
    app.add_exception_handler(
        UserPasswordNotMatchError,
        cast(ExceptionHandler, user_password_not_match_handler),
    )
    app.add_exception_handler(
        UrlAllreadyExistsError, cast(ExceptionHandler, url_allready_exists_handler)
    )
    app.add_exception_handler(
        UserIsNotAuthorizedError, cast(ExceptionHandler, user_is_not_authorized_handler)
    )
