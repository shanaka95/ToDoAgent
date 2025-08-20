"""
AI Agent Configuration - Setting Up Your Smart Assistant

This module contains all the configuration settings for your AI task assistant.
Think of it as the "control panel" that determines how your AI behaves,
which language model it uses, and what instructions it follows.

The configuration includes:
- Which AI model to use (like GPT-4, Claude, etc.)
- How creative vs. precise the AI should be (temperature)
- The instructions that tell the AI how to behave
- API keys and connection settings
- Logging and debugging options

The system prompt is particularly important - it's like the "job description"
that tells the AI exactly how to handle your task requests.
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

# Set up logging to track configuration issues
logger = logging.getLogger(__name__)


class AgentSettings(BaseSettings):
    """
    Configuration settings for your AI task assistant.
    
    This class holds all the settings that control how your AI assistant works.
    It uses environment variables for configuration, so you can easily change
    settings without modifying code.
    """
    
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="agent_",  # All environment variables start with "agent_"
        nested_model_default_partial_update=True,
        env_nested_delimiter="_",
    )

    # AI Model Configuration
    model_name: str = Field(
        default="gpt-4o-2024-08-06", 
        description="Which AI model to use (like GPT-4, Claude, etc.)"
    )
    temperature: float = Field(
        default=0.0, 
        description="How creative vs. precise the AI should be (0.0 = very precise, 1.0 = very creative)"
    )
    
    # API Connection Settings
    openai_base_url: str = Field(
        default="", 
        description="Base URL for the AI service (for OpenRouter or other providers)"
    )
    api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")  # Your API key for the AI service
    
    # Environment Settings
    environment: str = Field(
        default="development", 
        description="Current environment (development, production, etc.)"
    )
    
    # Logging and Debugging
    log_level: str = Field(
        default="INFO", 
        description="How detailed the logs should be"
    )
    enable_conversation_logging: bool = Field(
        default=True, 
        description="Whether to log conversations for debugging"
    )


# The AI's Job Description - This is crucial!
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


# Configuration Helper Functions
@lru_cache
def get_agent_settings() -> AgentSettings:
    """
    Get the AI agent's configuration settings.
    
    This function caches the settings so we don't have to reload them
    every time we need them. It's like keeping the settings in memory
    for quick access.
    
    Returns:
        The agent configuration settings
    """
    return AgentSettings()


@lru_cache
def get_app_settings() -> AppSettings:
    """
    Get the main application settings.
    
    Similar to agent settings, but for the overall application
    configuration like server settings, database connections, etc.
    
    Returns:
        The application configuration settings
    """
    return AppSettings()


@lru_cache
def get_model() -> BaseChatModel:
    """
    Create and configure the AI language model.
    
    This function sets up the AI model that will understand and respond
    to your requests. It uses the settings from AgentSettings to configure
    things like which model to use and how creative it should be.
    
    Returns:
        A configured AI language model ready to use
    """
    agent_settings = get_agent_settings()
    
    # Create the AI model with our configuration
    return ChatOpenAI(
        model=agent_settings.model_name,      # Which AI model to use
        temperature=agent_settings.temperature,  # How creative vs. precise
        api_key=agent_settings.api_key,       # Your API key
        base_url=agent_settings.openai_base_url  # Where to connect to
    )


@lru_cache
def get_system_prompt() -> ChatPromptTemplate:
    """
    Create the instructions that tell the AI how to behave.
    
    This function creates the "job description" for the AI. The system prompt
    is like a detailed instruction manual that tells the AI exactly how to
    handle different types of requests and what tools it can use.
    
    Returns:
        A prompt template with the AI's instructions
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_MESSAGE),  # The AI's job description
        ("placeholder", "{messages}"),  # Where user messages will go
    ])


def get_invoke_config(conversation_id: str) -> dict:
    """
    Create the configuration for running the AI agent.
    
    This function sets up the configuration that's used when we actually
    run the AI agent. It includes things like conversation tracking
    so the AI can remember previous messages in the same conversation.
    
    Args:
        conversation_id: A unique ID to track this conversation
        
    Returns:
        Configuration dictionary for the AI agent
    """
    agent_settings = get_agent_settings()

    # Set up the configuration with conversation tracking
    config = {
         "configurable": {"session_id": conversation_id}  # Track this conversation
    }

    return config

