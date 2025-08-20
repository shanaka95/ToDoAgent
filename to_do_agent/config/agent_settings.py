"""
Configuration settings for the ToDoAgent.

This module defines the configuration settings, model options, and prompts for the todo task management agent.
It uses Pydantic for settings management and validation.
"""

import logging
from functools import lru_cache
import os
from typing import ClassVar, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from to_do_agent.config.app_settings import AppSettings

# Configure logging
logger = logging.getLogger(__name__)


class AgentSettings(BaseSettings):
    """Configuration settings for the ToDo agent."""
    
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="agent_",
        nested_model_default_partial_update=True,
        env_nested_delimiter="_",
    )

    # Model configuration
    model_name: str = Field(default="gpt-4o-2024-08-06", description="Language model to use")
    temperature: float = Field(default=0.0, description="Model temperature")
    
    # OpenRouter configuration
    openai_base_url: str = Field(default="", description="OpenAI base URL")
    api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
    
    # Environment configuration
    environment: str = Field(default="development", description="Environment")
    
    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")
    enable_conversation_logging: bool = Field(default=True, description="Enable conversation logging")


# System prompt for the todo agent
SYSTEM_MESSAGE = """You are a ToDo Task Management Agent with context awareness. You understand conversation history and intelligently interpret user requests.

## Tools Available
- create_task_tool(task_name: str) - Create a new task
- get_all_tasks_tool() - List all tasks  
- update_task_tool(old_name: str, new_name: str) - Update task name
- delete_task_tool(task_name: str) - Delete a task
- check_task_exists_tool(task_name: str) - Check if task exists
- get_task_count_tool() - Get task count

## Core Behavior

### Context Awareness
- Analyze conversation history to understand context
- Infer complete task names from partial references
- "also X" or "and X" inherits previous action context

### Task Creation
- Extract task name from user input
- Check if task exists before creating
- Create multiple tasks when user mentions several items
- Handle sequential actions ("first X, then Y")

### Context Examples
- "buy biscuit" → "buy biscuit"
- "also eggs" → "buy eggs" (from shopping context)
- "clean kitchen" → "clean kitchen"  
- "also bathroom" → "clean bathroom" (from cleaning context)

### Multiple Tasks
- "buy bread first and then cheese" → creates both tasks
- "clean kitchen, buy groceries, call mom" → creates all three

### Task Management
- List tasks: Use get_all_tasks_tool
- Updates/Deletes: First list tasks, identify correct one, then execute
- Use conversation history to understand task references

### Greeting
- Empty: "Hello! I can help you keep track of your todo list. It's currently empty. Would you like to add anything?"
- With tasks: "Hello! I can help you keep track of your todo list. You have X tasks. Would you like to add anything?"

## Response Style
- Keep responses extremely short and direct
- Format: "Task 'name' added" or "Task 'name' already exists"
- For lists: show only task names
- Maximum 1-2 sentences

## Examples
- "buy milk" → "Task 'buy milk' added"
- "also eggs" → "Task 'buy eggs' added" (from shopping context)
- "show my tasks" → [list of tasks]
- "update milk to organic" → "Tasks: buy milk → Task 'buy milk' updated to 'buy organic milk'"

If uncertain about context, ask for clarification with a single short question.
"""


# Configuration and initialization functions
@lru_cache
def get_agent_settings() -> AgentSettings:
    """Get cached agent settings instance."""
    return AgentSettings()


@lru_cache
def get_app_settings() -> AppSettings:
    """Get cached app settings instance."""
    return AppSettings()


@lru_cache
def get_model() -> BaseChatModel:
    """Get cached language model instance."""
    agent_settings = get_agent_settings()
    
    return ChatOpenAI(
        model=agent_settings.model_name,
        temperature=agent_settings.temperature,
        api_key=agent_settings.api_key,
        base_url=agent_settings.openai_base_url
    )


@lru_cache
def get_system_prompt() -> ChatPromptTemplate:
    """Get cached system prompt template."""
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_MESSAGE),
        ("placeholder", "{messages}"),
    ])


def get_invoke_config(conversation_id: str) -> dict:
    """
    Get the invocation configuration for the agent.

    Args:
        conversation_id: Unique identifier for the conversation.

    Returns:
        Dict containing the invocation configuration.
    """
    agent_settings = get_agent_settings()

    config = {
         "configurable": {"session_id": conversation_id}
    }

    return config

