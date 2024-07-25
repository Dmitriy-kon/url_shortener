from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler

from app.services.common.exception import UserAlreadyExistsError, UserNotFoundError


async def user_not_found_handler(
    request: Request, exc: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


async def user_already_exists_handler(
    request: Request, exc: UserAlreadyExistsError
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
