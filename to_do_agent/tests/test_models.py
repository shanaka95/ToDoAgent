"""
Tests for the todo models.
"""

import pytest
from to_do_agent.domain.models.todo_models import Task, TaskListResponse, TaskResponse


class TestTask:
    """Test Task model."""
    
    def test_task_creation(self):
        """Test creating a task with name."""
        task = Task(name="Test Task")
        
        assert task.name == "Test Task"
    
    def test_task_creation_with_empty_name(self):
        """Test creating a task with empty name."""
        # Pydantic allows empty strings by default
        task = Task(name="")
        assert task.name == ""


class TestTaskListResponse:
    """Test TaskListResponse model."""
    
    def test_task_list_response_creation(self):
        """Test creating a task list response."""
        response = TaskListResponse(
            success=True,
            tasks=["Task 1", "Task 2", "Task 3"],
            total_count=3,
            message="Tasks retrieved successfully"
        )
        
        assert response.success is True
        assert response.tasks == ["Task 1", "Task 2", "Task 3"]
        assert response.total_count == 3
        assert response.message == "Tasks retrieved successfully"
    
    def test_task_list_response_empty(self):
        """Test creating a task list response with empty tasks."""
        response = TaskListResponse(
            success=True,
            tasks=[],
            total_count=0,
            message="No tasks found"
        )
        
        assert response.success is True
        assert response.tasks == []
        assert response.total_count == 0
        assert response.message == "No tasks found"


class TestTaskResponse:
    """Test TaskResponse model."""
    
    def test_task_response_creation(self):
        """Test creating a task response."""
        response = TaskResponse(
            success=True,
            task_name="Test Task",
            message="Task created successfully"
        )
        
        assert response.success is True
        assert response.task_name == "Test Task"
        assert response.message == "Task created successfully"
    
    def test_task_response_failure(self):
        """Test creating a task response for failure."""
        response = TaskResponse(
            success=False,
            task_name="",
            message="Task not found"
        )
        
        assert response.success is False
        assert response.task_name == ""
        assert response.message == "Task not found"
