from pydantic import BaseModel


class SUrlOut(BaseModel):
    urlid: int
    url: str
    short_url: str
    clics: int
