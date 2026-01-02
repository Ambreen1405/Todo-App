"""
Task service containing business logic for todo operations.
"""
from typing import List, Optional
from src.entities.task import Task, TaskStatus
from src.interfaces.task_repository import TaskRepository
import uuid


class TaskService:
    """Service layer for task management operations."""

    def __init__(self, task_repository: TaskRepository):
        """Initialize the service with a task repository."""
        self.task_repository = task_repository

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task with the given title and optional description."""
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status=TaskStatus.INCOMPLETE
        )
        return self.task_repository.add(task)

    def list_tasks(self) -> List[Task]:
        """Retrieve all tasks."""
        return self.task_repository.get_all()

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update an existing task with new title and/or description."""
        existing_task = self.task_repository.get_by_id(task_id)
        if not existing_task:
            return None

        # Update only provided fields, keep others unchanged
        if title is not None:
            existing_task.title = title
        if description is not None:
            existing_task.description = description

        return self.task_repository.update(existing_task)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        return self.task_repository.delete(task_id)

    def mark_task_complete(self, task_id: str) -> Optional[Task]:
        """Mark a task as complete."""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            return None
        task.mark_complete()
        return self.task_repository.update(task)

    def mark_task_incomplete(self, task_id: str) -> Optional[Task]:
        """Mark a task as incomplete."""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            return None
        task.mark_incomplete()
        return self.task_repository.update(task)