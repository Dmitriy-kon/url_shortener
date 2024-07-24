from fastapi import APIRouter

from app.routes.auth import auth_route
from app.routes.health_check import health_check_router
from app.routes.url import url_router

root_router = APIRouter()

root_router.include_router(health_check_router)

root_router.include_router(url_router)
root_router.include_router(auth_route)
