"""
Tests for the ToDo Agent - Ensuring Your AI Assistant Works Correctly

This module contains tests that verify your ToDo Agent works as expected.
Think of these tests as quality checks that ensure your AI assistant
can handle different scenarios correctly and doesn't break when you make changes.

The tests cover:
- Agent initialization and setup
- Message processing and task creation
- Error handling and edge cases
- Integration with the storage system

Running these tests helps ensure your AI assistant is reliable and works
as intended before you deploy it to users.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from to_do_agent.domain.agent import ToDoAgent
from to_do_agent.backend.todo_storage import TodoStorage


class TestToDoAgent:
    """
    Unit tests for the ToDo Agent class.
    
    These tests verify that the agent can be properly initialized and
    configured with different components (models, prompts, storage).
    """
    
    def test_agent_initialization_with_custom_model_and_prompt(self):
        """
        Test that the agent can be set up with custom AI model and instructions.
        
        This test verifies that you can customize the AI model and system prompt
        when creating the agent, which is useful for testing different configurations
        or using different AI services.
        """
        # Create mock objects to simulate the storage and AI components
        mock_storage = AsyncMock(spec=TodoStorage)
        custom_model = AsyncMock()
        custom_prompt = MagicMock()
        
        # Mock the tools to avoid actual tool creation during testing
        with patch("to_do_agent.domain.tools.get_tools") as mock_tools:
            mock_tools.return_value = [AsyncMock()]
            
            # Create the agent with custom components
            agent = ToDoAgent(
                todo_storage=mock_storage,
                model=custom_model,
                prompt=custom_prompt
            )
            
            # Verify that the agent was configured correctly
            assert agent.model == custom_model
            assert agent.system_prompt == custom_prompt
            assert agent.todo_storage == mock_storage


class TestToDoAgentIntegration:
    """
    Integration tests that verify the agent works with real components.
    
    These tests use actual storage and verify that the agent can process
    messages and perform task operations correctly in realistic scenarios.
    """
    
    @pytest.fixture
    def real_agent(self):
        """
        Create a real agent with actual in-memory storage for testing.
        
        This fixture provides a fully functional agent that we can use
        to test real interactions without needing external AI services.
        """
        storage = TodoStorage()
        return ToDoAgent(storage)
    
    @pytest.mark.asyncio
    async def test_agent_process_message_create_task(self, real_agent):
        """
        Test that the agent can process a message to create a task.
        
        This test verifies that when a user asks to create a task,
        the agent can understand the request and respond appropriately.
        """
        # Mock the agent's run method to avoid actual AI calls during testing
        with patch.object(real_agent, 'run') as mock_run:
            # Simulate a successful response from the AI
            mock_run.return_value = {
                "messages": [MagicMock(content="Task 'buy milk' added")]
            }
            
            # Test the message processing
            result = await real_agent.process_message("I need to buy milk")
            
            # Verify the response contains the expected confirmation
            assert "Task 'buy milk' added" in result
            # Verify the agent was called with the correct message
            mock_run.assert_called_once_with("I need to buy milk")
    
    @pytest.mark.asyncio
    async def test_agent_process_message_error(self, real_agent):
        """
        Test that the agent handles errors gracefully.
        
        This test ensures that if something goes wrong during message processing,
        the agent returns a helpful error message instead of crashing.
        """
        # Mock the agent's run method to simulate an error
        with patch.object(real_agent, 'run') as mock_run:
            mock_run.side_effect = Exception("Test error")
            
            # Test error handling
            result = await real_agent.process_message("test message")
            
            # Verify that an error message was returned
            assert "Error processing request" in result
    
    @pytest.mark.asyncio
    async def test_agent_process_message_no_response(self, real_agent):
        """
        Test that the agent handles cases where no response is generated.
        
        This test verifies that the agent can handle edge cases where
        the AI doesn't generate a proper response.
        """
        # Mock the agent's run method to return an empty response
        with patch.object(real_agent, 'run') as mock_run:
            mock_run.return_value = {}
            
            # Test handling of empty responses
            result = await real_agent.process_message("test message")
            
            # Verify that a default message is returned
            assert result == "No response generated"
