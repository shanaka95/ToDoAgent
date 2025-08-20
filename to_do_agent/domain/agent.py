"""
ToDo Agent Module 

This module contains the main AI agent that handles all todo task operations.
Think of it as a smart assistant that can understand natural language requests
and turn them into actions like creating, reading, updating, and deleting tasks.

The agent uses a language model (like GPT) to understand what users want,
then uses specialized tools to actually perform the task operations.
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

# Set up logging so we can see what's happening behind the scenes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToDoAgent:
    """
    The ToDo Agent - Your Smart Task Management Assistant
    
    This is the main class that handles all todo task operations. It's like having
    a personal assistant that can:
    - Understand natural language requests ("buy milk", "show my tasks")
    - Remember conversation context ("also eggs" means "buy eggs")
    - Perform task operations (create, read, update, delete)
    - Keep track of chat history for better context awareness
    
    The agent uses a language model to understand what you want, then uses
    specialized tools to actually perform the operations on your task list.
    """

    def __init__(
        self,
        todo_storage: TodoStorageInterface,
        model: Optional[BaseChatModel] = None,
        prompt: Optional[ChatPromptTemplate] = None,
    ) -> None:
        """
        Set up our smart task assistant with all the tools it needs.
        
        Args:
            todo_storage: Where we store and retrieve tasks (like a digital filing cabinet)
            model: The AI language model that understands natural language (defaults to GPT)
            prompt: Instructions that tell the AI how to behave (defaults to our custom prompt)
        """
        # Store our task database
        self.todo_storage = todo_storage
        
        # Set up the AI model that will understand user requests
        self.model = model or get_model()
        
        # Give the AI instructions on how to behave and what tools it can use
        self.system_prompt = prompt or get_system_prompt()
        
        # Set up logging to track what's happening
        self.logger = logging.getLogger(__name__)
        
        # Load our configuration settings
        self.settings = get_agent_settings()
        
        # Get all the tools the AI can use (create task, delete task, etc.)
        self.tools = get_tools(todo_storage)
        
        # Create the actual AI agent that combines the model, tools, and instructions
        self.agent = create_react_agent(self.model, self.tools, prompt=self.system_prompt)
        
        # Set up conversation memory so the AI can remember previous messages
        self.chat_history = ChatHistoryManager()

    async def run(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a user's request and return the AI's response.
        
        This is where the magic happens! The AI:
        1. Reads the user's message
        2. Looks at previous conversation history for context
        3. Decides what tools to use
        4. Performs the requested action
        5. Returns a helpful response
        
        Args:
            message: What the user wants (e.g., "buy milk", "show my tasks")
            conversation_id: A unique ID to keep track of this conversation

        Returns:
            The AI's response with the results of the requested action

        Raises:
            Exception: If something goes wrong during processing
        """
        # Use the provided conversation ID or default to 'default'
        conversation_id = conversation_id or 'default'
        invoke_config = get_invoke_config(conversation_id)

        try:
            self.logger.info(f"Processing todo request with conversation ID: {conversation_id}")
            
            # Get the conversation history so the AI has context
            history_messages = self.chat_history.get_conversation_messages(conversation_id)
            
            # Build the message list that we'll send to the AI
            messages = []
            
            # Add recent conversation history (last 10 messages for context)
            # This helps the AI understand things like "also eggs" means "buy eggs"
            recent_history = history_messages[-10:] if len(history_messages) > 10 else history_messages
            for msg in recent_history:
                if msg.role == "user":
                    messages.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    messages.append(AIMessage(content=msg.content))
            
            # Add the current user message
            messages.append(HumanMessage(content=message))
                        
            # Let the AI process the request with all the context
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
        Process a user message and return a friendly response.
        
        This is the main method that users interact with. It:
        1. Saves the user's message to conversation history
        2. Processes the request through the AI
        3. Saves the AI's response to history
        4. Returns a user-friendly response
        
        Args:
            message: The user's request
            conversation_id: Optional conversation ID for tracking context

        Returns:
            A friendly response from the AI assistant
        """
        conversation_id = conversation_id or 'default'
        
        try:
            # Save the user's message to our conversation history
            self.chat_history.add_message(conversation_id, message, "user")
            
            # Process the message through our AI agent
            result = await self.run(message, conversation_id)
            
            # Extract the AI's response from the result
            if result and "messages" in result:
                messages = result["messages"]
                if messages and hasattr(messages[-1], 'content'):
                    response_content = messages[-1].content
                    # Save the AI's response to conversation history
                    self.chat_history.add_message(conversation_id, response_content, "assistant")
                    return response_content
            return "No response generated"
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            error_message = f"Error processing request: {str(e)}"
            # Save the error message to conversation history
            self.chat_history.add_message(conversation_id, error_message, "assistant")
            return error_message


async def main() -> None:
    """
    Example of how to use the ToDo Agent.
    
    This function shows how to create and use the agent programmatically.
    It's useful for testing or if you want to use the agent in other applications.
    """
    from to_do_agent.backend.todo_storage import TodoStorage
    
    # Create a storage system for our tasks
    storage = TodoStorage()
    
    # Create our smart task assistant
    agent = ToDoAgent(storage)
    
    try:
        # Test the agent with a sample request
        result = await agent.run("Create a task called 'Buy groceries' with high priority")
        print(result)
    except Exception as e:
        logger.error(f"Error in example usage: {str(e)}")


# This block runs if someone executes this file directly
if __name__ == "__main__":
    asyncio.run(main())
