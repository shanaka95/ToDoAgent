"""
Chat API models for the ToDo Agent.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    
    message: str = Field(..., description="User message to send to the agent", min_length=1)
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for context")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    
    response: str = Field(..., description="Agent's response to the user message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for this interaction")
    success: bool = Field(True, description="Whether the request was successful")
    error: Optional[str] = Field(None, description="Error message if request failed")
