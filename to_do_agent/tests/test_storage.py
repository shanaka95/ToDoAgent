"""
Tests for the todo storage implementation.
"""

import pytest
from to_do_agent.backend.todo_storage import TodoStorage


class TestTodoStorage:
    """Test TodoStorage implementation."""
    
    @pytest.fixture
    def storage(self):
        """Create a fresh storage instance for each test."""
        return TodoStorage()
    
    @pytest.mark.asyncio
    async def test_create_task(self, storage):
        """Test creating a new task."""
        task_name = "Test Task"
        result = await storage.create_task(task_name)
        
        assert result == task_name
        tasks = await storage.get_all_tasks()
        assert task_name in tasks
    
    @pytest.mark.asyncio
    async def test_create_duplicate_task(self, storage):
        """Test creating a duplicate task should fail."""
        task_name = "Test Task"
        await storage.create_task(task_name)
        
        with pytest.raises(ValueError, match=f"Task '{task_name}' already exists"):
            await storage.create_task(task_name)
    
    @pytest.mark.asyncio
    async def test_create_duplicate_task_case_insensitive(self, storage):
        """Test creating a duplicate task with different case should fail."""
        task_name = "Test Task"
        await storage.create_task(task_name)
        
        with pytest.raises(ValueError, match=f"Task 'test task' already exists"):
            await storage.create_task("test task")
    
    @pytest.mark.asyncio
    async def test_get_task(self, storage):
        """Test getting a task by name."""
        task_name = "Test Task"
        await storage.create_task(task_name)
        
        result = await storage.get_task(task_name)
        assert result == task_name
    
    @pytest.mark.asyncio
    async def test_get_task_case_insensitive(self, storage):
        """Test getting a task by name with different case."""
        task_name = "Test Task"
        await storage.create_task(task_name)
        
        result = await storage.get_task("test task")
        assert result == task_name
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_task(self, storage):
        """Test getting a task that doesn't exist."""
        result = await storage.get_task("Nonexistent Task")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_all_tasks(self, storage):
        """Test getting all tasks."""
        task_names = ["Task 1", "Task 2", "Task 3"]
        
        for task_name in task_names:
            await storage.create_task(task_name)
        
        tasks = await storage.get_all_tasks()
        assert len(tasks) == 3
        for task_name in task_names:
            assert task_name in tasks
    
    @pytest.mark.asyncio
    async def test_get_all_tasks_empty(self, storage):
        """Test getting all tasks when storage is empty."""
        tasks = await storage.get_all_tasks()
        assert tasks == []
    
    @pytest.mark.asyncio
    async def test_update_task(self, storage):
        """Test updating a task name."""
        old_name = "Old Task"
        new_name = "New Task"
        
        await storage.create_task(old_name)
        result = await storage.update_task(old_name, new_name)
        
        assert result == new_name
        tasks = await storage.get_all_tasks()
        assert new_name in tasks
        assert old_name not in tasks
    
    @pytest.mark.asyncio
    async def test_update_task_case_insensitive(self, storage):
        """Test updating a task name with different case."""
        old_name = "Old Task"
        new_name = "New Task"
        
        await storage.create_task(old_name)
        result = await storage.update_task("old task", new_name)
        
        assert result == new_name
        tasks = await storage.get_all_tasks()
        assert new_name in tasks
        assert old_name not in tasks
    
    @pytest.mark.asyncio
    async def test_update_nonexistent_task(self, storage):
        """Test updating a task that doesn't exist."""
        result = await storage.update_task("Nonexistent Task", "New Task")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_task_to_existing_name(self, storage):
        """Test updating a task to a name that already exists."""
        task1 = "Task 1"
        task2 = "Task 2"
        
        await storage.create_task(task1)
        await storage.create_task(task2)
        
        with pytest.raises(ValueError, match=f"Task '{task2}' already exists"):
            await storage.update_task(task1, task2)
    
    @pytest.mark.asyncio
    async def test_delete_task(self, storage):
        """Test deleting a task."""
        task_name = "Test Task"
        await storage.create_task(task_name)
        
        result = await storage.delete_task(task_name)
        assert result is True
        
        tasks = await storage.get_all_tasks()
        assert task_name not in tasks
    
    @pytest.mark.asyncio
    async def test_delete_task_case_insensitive(self, storage):
        """Test deleting a task with different case."""
        task_name = "Test Task"
        await storage.create_task(task_name)
        
        result = await storage.delete_task("test task")
        assert result is True
        
        tasks = await storage.get_all_tasks()
        assert task_name not in tasks
    
    @pytest.mark.asyncio
    async def test_delete_nonexistent_task(self, storage):
        """Test deleting a task that doesn't exist."""
        result = await storage.delete_task("Nonexistent Task")
        assert result is False
    
    @pytest.mark.asyncio
    async def test_task_exists(self, storage):
        """Test checking if a task exists."""
        task_name = "Test Task"
        
        # Task doesn't exist initially
        exists = await storage.task_exists(task_name)
        assert exists is False
        
        # Create task
        await storage.create_task(task_name)
        
        # Task exists now
        exists = await storage.task_exists(task_name)
        assert exists is True
    
    @pytest.mark.asyncio
    async def test_task_exists_case_insensitive(self, storage):
        """Test checking if a task exists with different case."""
        task_name = "Test Task"
        await storage.create_task(task_name)
        
        exists = await storage.task_exists("test task")
        assert exists is True
