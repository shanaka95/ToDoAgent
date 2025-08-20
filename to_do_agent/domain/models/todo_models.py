from typing import List
from pydantic import BaseModel, Field


class Task(BaseModel):
    """Simple task model that only stores the task name"""
    
    name: str = Field(..., description="Task name")


class TaskListResponse(BaseModel):
    """Response model for task list"""
    
    success: bool = Field(..., description="Operation success status")
    tasks: List[str] = Field(..., description="List of task names")
    total_count: int = Field(..., description="Total number of tasks")
    message: str = Field(..., description="Response message")


class TaskResponse(BaseModel):
    """Response model for single task operations"""
    
    success: bool = Field(..., description="Operation success status")
    task_name: str = Field(..., description="Task name")
    message: str = Field(..., description="Response message")
