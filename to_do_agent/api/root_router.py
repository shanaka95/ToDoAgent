"""
Root API Router - The Main Entry Point for Your Web API

This module sets up the main API structure for your ToDo Agent application.
Think of it as the "directory" that organizes all your web endpoints and
routes incoming requests to the right handlers.

The root router:
- Defines the overall API structure
- Provides health check endpoints
- Organizes different API versions
- Sets up the main routes that users can access

This is what connects all your API endpoints together into a cohesive web service.
"""

from fastapi import APIRouter, Depends
from to_do_agent.api.v1.chat_router import router as chat_v1_router
from to_do_agent.config.dependencies import get_app_settings
from to_do_agent.config.app_settings import AppSettings
from to_do_agent.api.models.chat_models import HealthCheckResponse

# Create the main router that will hold all our API endpoints
router = APIRouter()


# Connect all the API endpoints together
# This line adds all the chat-related endpoints under the "/api/v1" path
router.include_router(chat_v1_router, prefix="/api/v1")


@router.get("/health", response_model=HealthCheckResponse)
def health_check(app_settings: AppSettings = Depends(get_app_settings)):
    """
    Check if your application is running properly.
    
    This endpoint lets you verify that your ToDo Agent is working correctly.
    It's useful for:
    - Monitoring systems to check if the app is alive
    - Load balancers to determine if the service is healthy
    - Developers to quickly verify the app is running
    
    Returns:
        Basic information about the service status and configuration
    """
    return HealthCheckResponse(
        status="healthy",
        service_name=app_settings.service_name,
        version=app_settings.version,
        environment=app_settings.environment,
    )
