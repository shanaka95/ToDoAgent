"""
ToDo Agent Module

This module implements an agent for handling todo task operations using a language model
and a set of specialized tools. The agent processes task-related requests, manages CRUD
operations, and provides natural language interface for todo management.
"""

import asyncio
import logging
import uuid
from typing import Dict, Any, Optional, List

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from to_do_agent.backend.todo_storage_interface import TodoStorageInterface
from to_do_agent.domain.tools import get_tools
from to_do_agent.domain.chat_history import ChatHistoryManager, ChatMessage, ChatConversation
from to_do_agent.config.agent_settings import (
    get_agent_settings,
    get_model,
    get_system_prompt,
    get_invoke_config
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToDoAgent:
    """
    Agent for handling todo task operations.

    This agent processes task-related requests using a language model and a set of tools.
    It handles task creation, retrieval, updates, and deletion through natural language.

    Attributes:
        model (BaseChatModel): Language model for decision making.
        tools (List[BaseTool]): Available task operation tools.
        system_prompt (ChatPromptTemplate): System prompt defining agent behavior.
        logger (logging.Logger): Logger instance for the agent.
        settings (AgentSettings): Agent configuration settings.
        todo_storage (TodoStorageInterface): Storage interface for task operations.
    """

    def __init__(
        self,
        todo_storage: TodoStorageInterface,
        model: Optional[BaseChatModel] = None,
        prompt: Optional[ChatPromptTemplate] = None,
    ) -> None:
        """
        Initialize the ToDoAgent.

        Args:
            todo_storage: Storage interface for task operations.
            model: The language model to use. Defaults to configured model.
            prompt: System prompt template. Defaults to configured prompt.
        """
        self.todo_storage = todo_storage
        self.model = model or get_model()
        self.system_prompt = prompt or get_system_prompt()
        self.logger = logging.getLogger(__name__)
        self.settings = get_agent_settings()
        self.tools = get_tools(todo_storage)
        self.agent = create_react_agent(self.model, self.tools, prompt=self.system_prompt)
        self.chat_history = ChatHistoryManager()

    async def run(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a task-related request and return the agent's response.

        Args:
            message: The input message or query for the agent.
            conversation_id: Optional conversation ID for maintaining context.

        Returns:
            Dict containing the agent's response with task operation results.

        Raises:
            Exception: If the agent fails to process the request.
        """
        # Use provided conversation_id or default to 'default'
        conversation_id = conversation_id or 'default'
        invoke_config = get_invoke_config(conversation_id)

        try:
            self.logger.info(f"Processing todo request with conversation ID: {conversation_id}")
            
            # Get chat history for context
            history_messages = self.chat_history.get_conversation_messages(conversation_id)
            
            # Build messages list with history context
            messages = []
            
            # Add recent history (last 10 messages for context)
            recent_history = history_messages[-10:] if len(history_messages) > 10 else history_messages
            for msg in recent_history:
                if msg.role == "user":
                    messages.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    messages.append(AIMessage(content=msg.content))
            
            # Add current message
            messages.append(HumanMessage(content=message))
                        
            # Use the pre-created agent with history context
            agent_response = await self.agent.ainvoke(
                {"messages": messages}, 
                config=invoke_config
            )

            self.logger.info(f"Successfully processed todo request")
            return agent_response

        except Exception as e:
            self.logger.error(
                f"Error processing todo request (conversation ID: {conversation_id}): {str(e)}"
            )
            raise



    async def process_message(self, message: str, conversation_id: Optional[str] = None) -> str:
        """
        Process a user message and return the response content.

        Args:
            message: The user's message.
            conversation_id: Optional conversation ID for maintaining context.

        Returns:
            The agent's response as a string.
        """
        conversation_id = conversation_id or 'default'
        
        try:
            # Add user message to chat history
            self.chat_history.add_message(conversation_id, message, "user")
            
            result = await self.run(message, conversation_id)
            if result and "messages" in result:
                messages = result["messages"]
                if messages and hasattr(messages[-1], 'content'):
                    response_content = messages[-1].content
                    # Add assistant response to chat history
                    self.chat_history.add_message(conversation_id, response_content, "assistant")
                    return response_content
            return "No response generated"
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            error_message = f"Error processing request: {str(e)}"
            # Add error message to chat history
            self.chat_history.add_message(conversation_id, error_message, "assistant")
            return error_message



async def main() -> None:
    """Example usage of the ToDoAgent."""
    from to_do_agent.backend.todo_storage import TodoStorage
    
    storage = TodoStorage()
    agent = ToDoAgent(storage)
    
    try:
        result = await agent.run("Create a task called 'Buy groceries' with high priority")
        print(result)
    except Exception as e:
        logger.error(f"Error in example usage: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
