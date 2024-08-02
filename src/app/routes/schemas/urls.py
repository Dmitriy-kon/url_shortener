from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, HttpUrl


class SUrlIn(BaseModel):
    url: HttpUrl


class SUrlInQuery(BaseModel):
    short: Annotated[str, Query()]


class SUrlOut(BaseModel):
    urlid: int
    url: str
    short_url: str
    clics: int
