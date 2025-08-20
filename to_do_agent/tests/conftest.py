"""
Pytest configuration and fixtures for to_do_agent tests.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from to_do_agent.backend.todo_storage import TodoStorage
from to_do_agent.domain.agent import ToDoAgent


@pytest.fixture
def sample_task_name():
    """Create a sample task name for testing."""
    return "Test Task"


@pytest.fixture
def mock_todo_storage():
    """Create a mock todo storage for testing."""
    storage = AsyncMock(spec=TodoStorage)
    
    # Mock the storage methods
    storage.create_task = AsyncMock()
    storage.get_task = AsyncMock()
    storage.get_all_tasks = AsyncMock()
    storage.update_task = AsyncMock()
    storage.delete_task = AsyncMock()
    storage.task_exists = AsyncMock()
    
    return storage


@pytest.fixture
def mock_agent(mock_todo_storage):
    """Create a mock agent for testing."""
    # Mock the model and prompt to avoid actual API calls
    with pytest.MonkeyPatch().context() as m:
        m.setattr("to_do_agent.config.agent_settings.get_model", MagicMock())
        m.setattr("to_do_agent.config.agent_settings.get_system_prompt", MagicMock())
        m.setattr("to_do_agent.config.agent_settings.get_agent_settings", MagicMock())
        
        agent = ToDoAgent(mock_todo_storage)
        return agent


@pytest.fixture
def real_agent():
    """Create a real agent with in-memory storage for integration tests."""
    storage = TodoStorage()
    return ToDoAgent(storage)


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
