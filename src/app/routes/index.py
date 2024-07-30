from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

index_route = APIRouter(tags=["index"])


templates = Jinja2Templates(directory="src/app/templates")


@index_route.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
