"""
Task Storage System

This module handles storing and retrieving your tasks. Think of it as a digital
filing cabinet where all your to-do items are kept safe and organized.

The storage system is responsible for:
- Saving new tasks when you create them
- Finding tasks when you ask about them
- Updating task names when you want to change them
- Removing tasks when you're done with them
- Keeping track of what tasks you already have

Currently, this uses a simple in-memory storage (like a sticky note that gets
erased when you restart the app). In a real application, this would connect
to a database to make your tasks permanent.
"""

from typing import List, Optional
from to_do_agent.backend.todo_storage_interface import TodoStorageInterface


class TodoStorage(TodoStorageInterface):
    """
    Simple in-memory storage for your tasks.
    
    This is like having a digital sticky note where you write down all your tasks.
    It's simple and fast, but the tasks disappear when you restart the app.
    
    In a real application, this would be replaced with a database connection
    to make your tasks permanent and accessible from anywhere.
    """
    
    def __init__(self):
        # Store tasks in a set (like a list but faster for checking if items exist)
        # A set is like a collection where each item can only appear once
        self.tasks: set[str] = set()
    
    async def create_task(self, task_name: str) -> str:
        """
        Add a new task to your list.
        
        This is like writing a new item on your to-do list. We check if the
        task already exists (ignoring case differences) to avoid duplicates.
        
        Args:
            task_name: The name of the task you want to add
            
        Returns:
            The name of the task that was created
            
        Raises:
            ValueError: If a task with this name already exists
        """
        # Check if this task already exists (case-insensitive)
        # This prevents you from accidentally creating "Buy milk" and "buy milk"
        if task_name.lower() in {task.lower() for task in self.tasks}:
            raise ValueError(f"Task '{task_name}' already exists")
        
        # Add the new task to our collection
        self.tasks.add(task_name)
        return task_name
    
    async def get_task(self, task_name: str) -> Optional[str]:
        """
        Find a specific task by name.
        
        This is like searching through your to-do list for a particular item.
        The search is case-insensitive, so "Buy Milk" and "buy milk" are treated
        as the same task.
        
        Args:
            task_name: The name of the task you're looking for
            
        Returns:
            The exact task name if found, or None if not found
        """
        # Search through all tasks (case-insensitive)
        for task in self.tasks:
            if task.lower() == task_name.lower():
                return task
        return None
    
    async def get_all_tasks(self) -> List[str]:
        """
        Get a list of all your current tasks.
        
        This is like looking at your entire to-do list to see everything
        you have to do. It returns all tasks in the order they were added.
        
        Returns:
            A list of all your current task names
        """
        # Convert our set back to a list for easier handling
        return list(self.tasks)
    
    async def update_task(self, old_name: str, new_name: str) -> Optional[str]:
        """
        Change the name of an existing task.
        
        This is like crossing out an old item on your list and writing
        a new one. We first find the exact task (case-insensitive), then
        replace it with the new name.
        
        Args:
            old_name: The current name of the task
            new_name: The new name you want to give it
            
        Returns:
            The new task name if successful, or None if the old task wasn't found
            
        Raises:
            ValueError: If a task with the new name already exists
        """
        # Find the exact task name (case-insensitive search)
        # We need to find the actual stored name to update it correctly
        actual_old_name = None
        for task in self.tasks:
            if task.lower() == old_name.lower():
                actual_old_name = task
                break
        
        # If we couldn't find the task, return None
        if not actual_old_name:
            return None
        
        # Check if the new name already exists (to avoid conflicts)
        # We exclude the current task from this check
        if new_name.lower() in {task.lower() for task in self.tasks if task != actual_old_name}:
            raise ValueError(f"Task '{new_name}' already exists")
        
        # Update the task name by removing the old one and adding the new one
        self.tasks.remove(actual_old_name)
        self.tasks.add(new_name)
        return new_name
    
    async def delete_task(self, task_name: str) -> bool:
        """
        Remove a task from your list.
        
        This is like crossing off a completed item or removing something
        you no longer need to do. The search is case-insensitive.
        
        Args:
            task_name: The name of the task you want to delete
            
        Returns:
            True if the task was found and deleted, False if it wasn't found
        """
        # Search through all tasks and remove the matching one
        # We use list() to create a copy so we can modify the set while iterating
        for task in list(self.tasks):
            if task.lower() == task_name.lower():
                self.tasks.remove(task)
                return True
        return False
    
    async def task_exists(self, task_name: str) -> bool:
        """
        Check if a task already exists in your list.
        
        This is like quickly scanning your to-do list to see if you already
        wrote down a particular item. Useful for avoiding duplicates.
        
        Args:
            task_name: The name of the task to check for
            
        Returns:
            True if the task exists, False if it doesn't
        """
        # Check if any task matches (case-insensitive)
        return task_name.lower() in {task.lower() for task in self.tasks}
