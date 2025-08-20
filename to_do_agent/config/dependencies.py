"""
Dependency Injection System

This module manages how all the different parts of your ToDo Agent application
are created and connected together. Think of it as the "wiring diagram" that
shows how all the components fit together.

The dependency injection system:
- Creates and manages all the services your app needs
- Ensures each service is created only once (singleton pattern)
- Provides a clean way to access services throughout the application
- Makes it easy to swap out different implementations (like changing storage systems)

This is what allows FastAPI to automatically provide the right services
to your API endpoints when they need them.
"""

from functools import lru_cache
from to_do_agent.config.app_settings import AppSettings
from to_do_agent.domain.agent import ToDoAgent
from to_do_agent.backend.todo_storage_interface import TodoStorageInterface
from to_do_agent.backend.todo_storage import TodoStorage


@lru_cache()
def get_app_settings() -> AppSettings:
    """
    Get the application settings (configuration).
    
    This function provides access to all your app's configuration settings.
    It uses caching (@lru_cache) so the settings are only loaded once,
    making the app faster and more efficient.
    
    Returns:
        The application configuration settings
    """
    return AppSettings()


@lru_cache()
def get_todo_storage() -> TodoStorageInterface:
    """
    Get the task storage system.
    
    This function creates and provides access to the system that stores
    your tasks. It uses caching so the storage system is created only once,
    ensuring all parts of the app use the same storage.
    
    Returns:
        The task storage system (where your tasks are saved)
    """
    return TodoStorage()


@lru_cache()
def get_to_do_agent() -> ToDoAgent:
    """
    Get the AI task assistant.
    
    This function creates and provides access to your AI assistant.
    It automatically connects the AI to the task storage system so
    the AI can save and retrieve your tasks.
    
    This is the main service that handles all your task management requests.
    
    Returns:
        Your configured AI task assistant
    """
    # Get the storage system first
    todo_storage = get_todo_storage()
    
    # Create the AI agent with the storage system
    return ToDoAgent(todo_storage=todo_storage)
