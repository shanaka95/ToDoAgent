from fastapi import APIRouter, Depends
from to_do_agent.api.v1.chat_router import router as chat_v1_router
from to_do_agent.config.dependencies import get_app_settings
from to_do_agent.config.app_settings import AppSettings
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    service_name: str
    version: str
    environment: str = "development"
    timestamp: datetime = datetime.now()


# Mount v1 API endpoints
router.include_router(chat_v1_router, prefix="/api/v1")


@router.get("/health", response_model=HealthCheckResponse)
def health_check(app_settings: AppSettings = Depends(get_app_settings)):
    """
    Health check endpoint for the service.
    Returns service status and basic information.
    """
    return HealthCheckResponse(
        status="healthy",
        service_name=app_settings.service_name,
        version=app_settings.version,
        environment=app_settings.environment,
    )
