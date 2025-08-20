"""
Task Storage Interface - The Contract for Storing Tasks

This module defines the interface (contract) that any task storage system
must follow. Think of it as a "job description" that specifies exactly
what operations any storage system must be able to perform.

The interface ensures that:
- All storage systems work the same way
- You can easily swap out different storage implementations
- The AI agent doesn't need to know how storage works internally
- You can test the system with different storage backends

This is an abstract interface - it defines WHAT operations are available,
but not HOW they're implemented. The actual implementation could use
a database, file system, cloud storage, or anything else.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class TodoStorageInterface(ABC):
    """
    The contract that all task storage systems must follow.
    
    This abstract class defines all the operations that any storage system
    must provide. It's like a blueprint that ensures all storage systems
    work consistently, regardless of how they're implemented.
    
    Any class that implements this interface can be used by the AI agent
    to store and retrieve tasks.
    """
    
    @abstractmethod
    async def create_task(self, task_name: str) -> str:
        """
        Add a new task to storage.
        
        This method must be able to save a new task with the given name.
        It should return the name of the task that was created.
        
        Args:
            task_name: The name of the task to create
            
        Returns:
            The name of the task that was created
        """
        pass
    
    @abstractmethod
    async def get_task(self, task_name: str) -> Optional[str]:
        """
        Find a specific task by name.
        
        This method must be able to search for and return a task
        with the given name. If the task doesn't exist, it should
        return None.
        
        Args:
            task_name: The name of the task to find
            
        Returns:
            The task name if found, or None if not found
        """
        pass
    
    @abstractmethod
    async def get_all_tasks(self) -> List[str]:
        """
        Get a list of all stored tasks.
        
        This method must return all tasks currently stored in the system.
        It should return an empty list if no tasks exist.
        
        Returns:
            A list of all task names
        """
        pass
    
    @abstractmethod
    async def update_task(self, old_name: str, new_name: str) -> Optional[str]:
        """
        Change the name of an existing task.
        
        This method must be able to find a task with the old name and
        change it to the new name. If the old task doesn't exist,
        it should return None.
        
        Args:
            old_name: The current name of the task
            new_name: The new name for the task
            
        Returns:
            The new task name if successful, or None if the old task wasn't found
        """
        pass
    
    @abstractmethod
    async def delete_task(self, task_name: str) -> bool:
        """
        Remove a task from storage.
        
        This method must be able to find and remove a task with the given name.
        It should return True if the task was found and deleted, False if it wasn't found.
        
        Args:
            task_name: The name of the task to delete
            
        Returns:
            True if the task was deleted, False if it wasn't found
        """
        pass
    
    @abstractmethod
    async def task_exists(self, task_name: str) -> bool:
        """
        Check if a task exists in storage.
        
        This method must be able to quickly check whether a task with
        the given name exists in the storage system.
        
        Args:
            task_name: The name of the task to check for
            
        Returns:
            True if the task exists, False if it doesn't
        """
        pass
