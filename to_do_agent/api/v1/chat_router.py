import logging
from fastapi import APIRouter, Depends, HTTPException

from to_do_agent.config.dependencies import get_to_do_agent
from to_do_agent.domain.agent import ToDoAgent
from to_do_agent.api.models.chat_models import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    agent: ToDoAgent = Depends(get_to_do_agent),
):
    """
    Chat with the ToDo agent.
    
    Send a message to the agent and receive a response. The agent can help you:
    - Create new tasks
    - View existing tasks
    - Update task details
    - Delete tasks
    - Get task recommendations
    
    Examples:
    - "Create a task called 'Buy groceries' with high priority"
    - "Show me all my tasks"
    - "Update task abc123 to be completed"
    - "Delete the grocery task"
    """
    try:
        logger.info(f"Processing chat request: {request.message[:100]}...")
        
        # Process the message through the agent with conversation context
        response_text = await agent.process_message(request.message, request.conversation_id)
        
        return ChatResponse(
            response=response_text,
            conversation_id=request.conversation_id,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        
        return ChatResponse(
            response="I'm sorry, I encountered an error processing your request. Please try again.",
            conversation_id=request.conversation_id,
            success=False,
            error=str(e)
        )
