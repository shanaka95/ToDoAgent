"""
Chat API Router - The Web Interface for Your AI Assistant

This module handles the web API that lets you talk to your AI task assistant
through HTTP requests. Think of it as the "front door" to your AI assistant
that anyone on the internet can use.

When you send a message to this endpoint, it:
1. Receives your request
2. Passes it to the AI agent
3. Gets the AI's response
4. Sends it back to you

This is what makes your AI assistant accessible through web browsers,
mobile apps, or any other application that can make HTTP requests.
"""

import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException

from to_do_agent.config.dependencies import get_to_do_agent
from to_do_agent.domain.agent import ToDoAgent
from to_do_agent.api.models.chat_models import ChatRequest, ChatResponse

# Set up logging so we can track what's happening
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    agent: ToDoAgent = Depends(get_to_do_agent),
):
    """
    Chat with your AI task assistant through the web.
    
    This is the main endpoint that lets you talk to your AI assistant.
    You can send natural language requests like:
    - "Create a task called 'Buy groceries' with high priority"
    - "Show me all my tasks"
    - "Update task abc123 to be completed"
    - "Delete the grocery task"
    
    The AI will understand your request, perform the appropriate action,
    and send back a helpful response.
    
    Args:
        request: Contains your message and conversation ID
        agent: The AI assistant (automatically provided by FastAPI)
        
    Returns:
        A response with the AI's reply and conversation tracking info
    """
    try:
        # Log the incoming request (first 100 characters to avoid huge logs)
        logger.info(f"Processing chat request: {request.message[:100]}...")

        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Send the message to our AI agent and get a response
        # The agent will handle all the AI processing and task management
        response_text = await agent.process_message(request.message, conversation_id)
        
        # Package up the response with success status and conversation tracking
        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            success=True
        )
        
    except Exception as e:
        # If something goes wrong, log the error and return a friendly message
        logger.error(f"Error processing chat request: {str(e)}")
        
        # Return an error response that's user-friendly
        return ChatResponse(
            response="I'm sorry, I encountered an error processing your request. Please try again.",
            conversation_id=conversation_id,
            success=False,
            error=str(e)
        )
