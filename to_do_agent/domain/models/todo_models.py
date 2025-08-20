"""
Task Data Models - Defining Your To-Do Items

This module defines the structure of task data in your ToDo Agent application.
Think of these as the "blueprints" that specify what information is stored
about each task and how task-related responses are formatted.

The models ensure that:
- Task data is consistent and well-structured
- API responses include all necessary information
- Task operations return predictable results
- The system knows exactly what a "task" looks like

These models are used throughout the application to ensure data consistency
and provide clear interfaces for task operations.
"""

from typing import List
from pydantic import BaseModel, Field


class Task(BaseModel):
    """
    A single task in your to-do list.
    
    This represents one item on your task list. Currently, it only stores
    the task name, but could be extended to include things like:
    - Priority level
    - Due date
    - Description
    - Status (completed, in progress, etc.)
    """
    
    name: str = Field(
        ..., 
        description="The name or title of the task (e.g., 'Buy groceries', 'Call mom')"
    )


class TaskListResponse(BaseModel):
    """
    Response when you ask to see all your tasks.
    
    This is what you get back when you request a list of all your tasks.
    It includes the tasks themselves, a count of how many you have,
    and a message explaining what happened.
    """
    
    success: bool = Field(
        ..., 
        description="Whether the request to get your tasks was successful"
    )
    tasks: List[str] = Field(
        ..., 
        description="A list of all your current task names"
    )
    total_count: int = Field(
        ..., 
        description="How many tasks you currently have in total"
    )
    message: str = Field(
        ..., 
        description="A human-readable message explaining the result"
    )


class TaskResponse(BaseModel):
    """
    Response for operations on a single task.
    
    This is what you get back when you perform an operation on one specific
    task, like creating, updating, or deleting a task. It tells you whether
    the operation succeeded and provides details about what happened.
    """
    
    success: bool = Field(
        ..., 
        description="Whether the task operation was successful"
    )
    task_name: str = Field(
        ..., 
        description="The name of the task that was operated on"
    )
    message: str = Field(
        ..., 
        description="A human-readable message explaining what happened to the task"
    )
