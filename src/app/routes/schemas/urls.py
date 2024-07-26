from pydantic import BaseModel


class SUrlIn(BaseModel):
    url: str



class SUrlOut(BaseModel):
    urlid: int
    url: str
    short_url: str
    clics: int
