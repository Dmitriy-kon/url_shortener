from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler

from app.services.common.exception import UserNotFoundError


async def user_not_found_handler(
    request: Request, exc: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UserNotFoundError, cast(ExceptionHandler, user_not_found_handler))
