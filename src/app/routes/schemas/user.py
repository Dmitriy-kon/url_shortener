from typing import Annotated

from pydantic import BaseModel, Field

from app.routes.schemas.urls import SUrlOut


class SUserIn(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: Annotated[str, Field(min_length=8)]


class SUserOut(BaseModel):
    username: str
    urls: list[SUrlOut] | None
