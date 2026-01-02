"""
In-memory repository for Task entities.
"""
from typing import Dict, List, Optional
from src.entities.task import Task


class TaskRepository:
    """In-memory repository for managing Task entities."""

    def __init__(self):
        """Initialize the repository with an empty storage."""
        self._tasks: Dict[str, Task] = {}

    def add(self, task: Task) -> Task:
        """Add a new task to the repository."""
        self._tasks[task.id] = task
        return task

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)

    def get_all(self) -> List[Task]:
        """Retrieve all tasks."""
        return list(self._tasks.values())

    def update(self, task: Task) -> Optional[Task]:
        """Update an existing task."""
        if task.id not in self._tasks:
            return None
        self._tasks[task.id] = task
        return task

    def delete(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False