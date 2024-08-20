from dataclasses import dataclass, field

from fastapi import APIRouter

health_check_router = APIRouter(tags=["health-check"], prefix="/health-check")


@dataclass
class HealthCheckResponse:
    status: str = field(default="Ok")


@health_check_router.get("/")
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="Ok")
