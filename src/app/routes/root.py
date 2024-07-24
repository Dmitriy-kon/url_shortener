from fastapi import APIRouter

from app.routes.health_check import health_check_router

root_router = APIRouter()

root_router.include_router(health_check_router)
