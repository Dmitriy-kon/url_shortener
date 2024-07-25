from pydantic import BaseModel


class SUrlIn(BaseModel):
    url: str
    user_id: int | None


class SUrlOut(BaseModel):
    urlid: int
    url: str
    short_url: str
    clics: int
