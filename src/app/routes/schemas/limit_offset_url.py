from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class SLimitOffsetUrl(BaseModel):
    limit: Annotated[int, Query(ge=1, le=30, default=10)]
    offset: Annotated[int, Query(ge=0, default=0)]
