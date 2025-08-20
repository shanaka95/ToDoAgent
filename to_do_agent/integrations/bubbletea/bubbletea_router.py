"""
BubbleTea Integration Router - External Chat Interface

This module provides the API endpoints for BubbleTea integration.
Based on the BubbleTea documentation and the logs showing POST to /bubbletea,
the required endpoints are:
- GET /bubbletea/config - Provides bot configuration  
- POST /bubbletea - Handles chat messages (not /bubbletea/chat)

This router is mounted under /bubbletea prefix in the main app.
"""

from fastapi import APIRouter
from to_do_agent.integrations.bubbletea.bubbletea_endpoints import fastapi_config_handler, fastapi_chat_handler, ChatRequest

# Create router with /bubbletea prefix
router = APIRouter(
    tags=["bubbletea"],  # Group these endpoints in API docs
    responses={404: {"description": "Not found"}},
)

@router.get("/config")
async def bubbletea_config():
    """
    Provide configuration info to BubbleTea.
    
    This endpoint returns the bot configuration that BubbleTea needs
    to display your bot properly in their interface.
    """
    return fastapi_config_handler()

@router.post("/chat")
async def bubbletea_chat(req: ChatRequest):
    """
    Handle chat requests from BubbleTea.
    
    This endpoint processes messages from BubbleTea users and returns
    responses in the format that BubbleTea expects.
    
    Note: BubbleTea sends POST requests to /bubbletea (not /bubbletea/chat)
    """
    return await fastapi_chat_handler(req)

