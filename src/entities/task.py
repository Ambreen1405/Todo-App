"""
Task entity representing a todo item in the system.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import uuid


class TaskStatus(Enum):
    """Status of a task"""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


@dataclass
class Task:
    """Represents a todo task with ID, title, description, and status."""

    id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.INCOMPLETE

    def __post_init__(self):
        """Validate task after initialization."""
        if not self.id:
            raise ValueError("Task ID cannot be empty")
        if not self.title:
            raise ValueError("Task title cannot be empty")

    def mark_complete(self):
        """Mark the task as complete."""
        self.status = TaskStatus.COMPLETE

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.status = TaskStatus.INCOMPLETE

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value
        }