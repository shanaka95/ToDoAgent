from abc import ABC, abstractmethod
from typing import List, Optional


class TodoStorageInterface(ABC):
    """Interface for todo storage operations."""
    
    @abstractmethod
    async def create_task(self, task_name: str) -> str:
        """Create a new task with the given name."""
        pass
    
    @abstractmethod
    async def get_task(self, task_name: str) -> Optional[str]:
        """Get a task by name."""
        pass
    
    @abstractmethod
    async def get_all_tasks(self) -> List[str]:
        """Get all task names."""
        pass
    
    @abstractmethod
    async def update_task(self, old_name: str, new_name: str) -> Optional[str]:
        """Update a task name."""
        pass
    
    @abstractmethod
    async def delete_task(self, task_name: str) -> bool:
        """Delete a task by name."""
        pass
    
    @abstractmethod
    async def task_exists(self, task_name: str) -> bool:
        """Check if a task exists by name."""
        pass
