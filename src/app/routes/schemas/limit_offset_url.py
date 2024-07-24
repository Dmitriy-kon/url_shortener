from typing import Annotated

from pydantic import BaseModel, Field


class SLimitOffsetUrl(BaseModel):
    limit: Annotated[int, Field(ge=1, le=30, default=10)]
    offset: Annotated[int, Field(ge=0, default=0)]
    user_id: int
