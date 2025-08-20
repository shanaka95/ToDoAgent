from functools import lru_cache
from to_do_agent.config.app_settings import AppSettings
from to_do_agent.domain.agent import ToDoAgent
from to_do_agent.backend.todo_storage_interface import TodoStorageInterface
from to_do_agent.backend.todo_storage import TodoStorage


@lru_cache()
def get_app_settings() -> AppSettings:
    """Get application settings singleton."""
    return AppSettings()


@lru_cache()
def get_todo_storage() -> TodoStorageInterface:
    """Get todo storage singleton."""
    return TodoStorage()


@lru_cache()
def get_to_do_agent() -> ToDoAgent:
    """Get to-do agent singleton."""
    todo_storage = get_todo_storage()
    return ToDoAgent(todo_storage=todo_storage)
