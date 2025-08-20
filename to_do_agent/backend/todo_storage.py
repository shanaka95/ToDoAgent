from typing import List, Optional
from to_do_agent.backend.todo_storage_interface import TodoStorageInterface


class TodoStorage(TodoStorageInterface):
    """In-memory todo storage implementation that only stores task names."""
    
    def __init__(self):
        self.tasks: set[str] = set()
    
    async def create_task(self, task_name: str) -> str:
        """Create a new task."""
        if task_name.lower() in {task.lower() for task in self.tasks}:
            raise ValueError(f"Task '{task_name}' already exists")
        
        self.tasks.add(task_name)
        return task_name
    
    async def get_task(self, task_name: str) -> Optional[str]:
        """Get a task by name."""
        for task in self.tasks:
            if task.lower() == task_name.lower():
                return task
        return None
    
    async def get_all_tasks(self) -> List[str]:
        """Get all task names."""
        return list(self.tasks)
    
    async def update_task(self, old_name: str, new_name: str) -> Optional[str]:
        """Update a task name."""
        # Find the exact task name (case-insensitive search)
        actual_old_name = None
        for task in self.tasks:
            if task.lower() == old_name.lower():
                actual_old_name = task
                break
        
        if not actual_old_name:
            return None
        
        # Check if new name already exists
        if new_name.lower() in {task.lower() for task in self.tasks if task != actual_old_name}:
            raise ValueError(f"Task '{new_name}' already exists")
        
        # Update the task name
        self.tasks.remove(actual_old_name)
        self.tasks.add(new_name)
        return new_name
    
    async def delete_task(self, task_name: str) -> bool:
        """Delete a task by name."""
        for task in list(self.tasks):
            if task.lower() == task_name.lower():
                self.tasks.remove(task)
                return True
        return False
    
    async def task_exists(self, task_name: str) -> bool:
        """Check if a task exists by name."""
        return task_name.lower() in {task.lower() for task in self.tasks}
