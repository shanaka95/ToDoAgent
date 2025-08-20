"""
Chat API Data Models - Defining How Data Flows

This module defines the structure of data that flows between your web application
and the AI assistant. Think of these as the "contracts" that specify exactly
what information is sent and received when you talk to the AI.

The models ensure that:
- All required data is provided
- Data is in the correct format
- API responses are consistent and predictable
- The web interface knows exactly what to expect

These models are used by FastAPI to automatically validate incoming requests
and format outgoing responses.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """
    The structure of a chat request from a user.
    
    This defines what information is needed when someone wants to
    send a message to the AI assistant. It's like the envelope that
    contains your message and any additional context.
    """
    
    message: str = Field(
        ..., 
        description="The message you want to send to the AI assistant (must not be empty)",
        min_length=1
    )
    conversation_id: Optional[str] = Field(
        None, 
        description="Optional ID to track this conversation (helps the AI remember context)"
    )


class ChatResponse(BaseModel):
    """
    The structure of a response from the AI assistant.
    
    This defines what information the AI sends back to you after
    processing your request. It includes the AI's response, conversation
    tracking, and whether the request was successful.
    """
    
    response: str = Field(
        ..., 
        description="The AI assistant's reply to your message"
    )
    conversation_id: Optional[str] = Field(
        None, 
        description="The conversation ID (same as in your request, for tracking)"
    )
    success: bool = Field(
        True, 
        description="Whether the AI successfully processed your request"
    )
    error: Optional[str] = Field(
        None, 
        description="If something went wrong, this explains what the problem was"
    )

class HealthCheckResponse(BaseModel):
    """
    Response structure for health check requests.
    
    This defines what information is returned when someone checks
    if your application is running properly. It includes basic
    information about the service status and configuration.
    """
    status: str = Field(description="Whether the service is healthy")
    service_name: str = Field(description="The name of your application")
    version: str = Field(description="Current version of the application")
    environment: str = Field(default="development", description="Current environment")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the health check was performed")
