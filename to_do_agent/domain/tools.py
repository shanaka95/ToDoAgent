"""
ToDo Agent Tools Module

This module contains all the tools available to the ToDo agent for managing tasks.
Each tool is designed to handle specific CRUD operations on todo tasks.
"""

import logging
from typing import List

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


def create_todo_tools(todo_storage):
    """Create todo tools with storage dependency."""
    
    @tool
    async def create_task_tool(task_name: str) -> str:
        """Create a new task with the given name"""
        try:
            # Check if task already exists
            if await todo_storage.task_exists(task_name):
                return f"Task '{task_name}' already exists"
            
            await todo_storage.create_task(task_name)
            return f"Task '{task_name}' added"
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return f"Error creating task: {str(e)}"

    @tool
    async def get_task_tool(task_name: str) -> str:
        """Get a specific task by name"""
        try:
            task = await todo_storage.get_task(task_name)
            if task:
                return f"Task found: {task}"
            else:
                return f"Task '{task_name}' not found"
        except Exception as e:
            logger.error(f"Error retrieving task: {str(e)}")
            return f"Error retrieving task: {str(e)}"

    @tool
    async def get_all_tasks_tool() -> str:
        """Get all tasks"""
        try:
            tasks = await todo_storage.get_all_tasks()
            
            if not tasks:
                return "No tasks found"
            
            return f"Tasks: {', '.join(tasks)}"
        except Exception as e:
            logger.error(f"Error retrieving tasks: {str(e)}")
            return f"Error retrieving tasks: {str(e)}"

    @tool
    async def update_task_tool(old_name: str, new_name: str) -> str:
        """Update an existing task name"""
        try:
            task = await todo_storage.update_task(old_name, new_name)
            
            if task:
                return f"Task '{old_name}' updated to '{new_name}'"
            else:
                return f"Task '{old_name}' not found"
        except ValueError as e:
            return str(e)
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}")
            return f"Error updating task: {str(e)}"

    @tool
    async def delete_task_tool(task_name: str) -> str:
        """Delete a task by name"""
        try:
            success = await todo_storage.delete_task(task_name)
            if success:
                return f"Task '{task_name}' deleted"
            else:
                return f"Task '{task_name}' not found"
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}")
            return f"Error deleting task: {str(e)}"

    @tool
    async def check_task_exists_tool(task_name: str) -> str:
        """Check if a task exists by name"""
        try:
            exists = await todo_storage.task_exists(task_name)
            if exists:
                return f"Task '{task_name}' exists"
            else:
                return f"Task '{task_name}' does not exist"
        except Exception as e:
            logger.error(f"Error checking task: {str(e)}")
            return f"Error checking task: {str(e)}"

    @tool
    async def get_task_count_tool() -> str:
        """Get the total number of tasks"""
        try:
            tasks = await todo_storage.get_all_tasks()
            count = len(tasks)
            return str(count)
        except Exception as e:
            logger.error(f"Error getting task count: {str(e)}")
            return "0"

    return [
        create_task_tool,
        get_task_tool,
        get_all_tasks_tool,
        update_task_tool,
        delete_task_tool,
        check_task_exists_tool,
        get_task_count_tool
    ]


def get_tools(todo_storage) -> List:
    """Get all available tools for the ToDo agent."""
    return create_todo_tools(todo_storage)
