"""
Tests for the main ToDo agent.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from to_do_agent.domain.agent import ToDoAgent
from to_do_agent.backend.todo_storage import TodoStorage


class TestToDoAgent:
    """Test ToDoAgent implementation."""
    
    def test_agent_initialization_with_custom_model_and_prompt(self):
        """Test agent initialization with custom model and prompt."""
        mock_storage = AsyncMock(spec=TodoStorage)
        custom_model = AsyncMock()
        custom_prompt = MagicMock()
        
        with patch("to_do_agent.domain.tools.get_tools") as mock_tools:
            mock_tools.return_value = [AsyncMock()]
            
            agent = ToDoAgent(
                todo_storage=mock_storage,
                model=custom_model,
                prompt=custom_prompt
            )
            
            assert agent.model == custom_model
            assert agent.system_prompt == custom_prompt
            assert agent.todo_storage == mock_storage


class TestToDoAgentIntegration:
    """Integration tests for ToDoAgent with real storage."""
    
    @pytest.fixture
    def real_agent(self):
        """Create a real agent with in-memory storage."""
        storage = TodoStorage()
        return ToDoAgent(storage)
    
    @pytest.mark.asyncio
    async def test_agent_process_message_create_task(self, real_agent):
        """Test agent processing a message to create a task."""
        # Mock the agent's run method to avoid actual LLM calls
        with patch.object(real_agent, 'run') as mock_run:
            mock_run.return_value = {
                "messages": [MagicMock(content="Task 'buy milk' added")]
            }
            
            result = await real_agent.process_message("I need to buy milk")
            
            assert "Task 'buy milk' added" in result
            mock_run.assert_called_once_with("I need to buy milk")
    
    @pytest.mark.asyncio
    async def test_agent_process_message_error(self, real_agent):
        """Test agent processing a message with error."""
        with patch.object(real_agent, 'run') as mock_run:
            mock_run.side_effect = Exception("Test error")
            
            result = await real_agent.process_message("test message")
            
            assert "Error processing request" in result
    
    @pytest.mark.asyncio
    async def test_agent_process_message_no_response(self, real_agent):
        """Test agent processing a message with no response."""
        with patch.object(real_agent, 'run') as mock_run:
            mock_run.return_value = {}
            
            result = await real_agent.process_message("test message")
            
            assert result == "No response generated"
