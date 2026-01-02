"""
Unit tests for the TaskService.
"""
import pytest
from src.entities.task import Task, TaskStatus
from src.interfaces.task_repository import TaskRepository
from src.use_cases.task_service import TaskService


class TestTaskService:
    """Test cases for the TaskService."""

    def setup_method(self):
        """Set up a fresh TaskService for each test."""
        self.task_repository = TaskRepository()
        self.task_service = TaskService(self.task_repository)

    def test_add_task_creates_task_with_correct_properties(self):
        """Test that adding a task creates it with correct properties."""
        task = self.task_service.add_task("Test Title", "Test Description")

        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.status == TaskStatus.INCOMPLETE
        assert task.id is not None
        assert len(task.id) > 0

    def test_add_task_without_description_creates_task_with_none_description(self):
        """Test that adding a task without description sets description to None."""
        task = self.task_service.add_task("Test Title")

        assert task.title == "Test Title"
        assert task.description is None
        assert task.status == TaskStatus.INCOMPLETE

    def test_list_tasks_returns_empty_list_when_no_tasks(self):
        """Test that listing tasks returns an empty list when there are no tasks."""
        tasks = self.task_service.list_tasks()

        assert tasks == []

    def test_list_tasks_returns_all_tasks(self):
        """Test that listing tasks returns all added tasks."""
        task1 = self.task_service.add_task("Task 1")
        task2 = self.task_service.add_task("Task 2")

        tasks = self.task_service.list_tasks()

        assert len(tasks) == 2
        assert task1 in tasks
        assert task2 in tasks

    def test_update_task_updates_provided_fields_only(self):
        """Test that updating a task only updates provided fields."""
        original_task = self.task_service.add_task("Original Title", "Original Description")

        updated_task = self.task_service.update_task(
            original_task.id,
            title="New Title"
            # Not updating description
        )

        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged
        assert updated_task.id == original_task.id  # ID should remain unchanged

    def test_update_task_returns_none_if_task_not_found(self):
        """Test that updating a non-existent task returns None."""
        result = self.task_service.update_task("non-existent-id", title="New Title")

        assert result is None

    def test_update_task_with_all_fields(self):
        """Test that updating a task with all fields works correctly."""
        original_task = self.task_service.add_task("Original Title", "Original Description")

        updated_task = self.task_service.update_task(
            original_task.id,
            title="New Title",
            description="New Description"
        )

        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_delete_task_returns_true_when_task_exists(self):
        """Test that deleting an existing task returns True."""
        task = self.task_service.add_task("Test Title")

        result = self.task_service.delete_task(task.id)

        assert result is True

    def test_delete_task_returns_false_when_task_does_not_exist(self):
        """Test that deleting a non-existent task returns False."""
        result = self.task_service.delete_task("non-existent-id")

        assert result is False

    def test_delete_task_removes_task_from_repository(self):
        """Test that deleting a task removes it from the repository."""
        task = self.task_service.add_task("Test Title")

        # Verify task exists
        tasks = self.task_service.list_tasks()
        assert len(tasks) == 1

        # Delete task
        self.task_service.delete_task(task.id)

        # Verify task is gone
        tasks = self.task_service.list_tasks()
        assert len(tasks) == 0

    def test_mark_task_complete_marks_task_as_complete(self):
        """Test that marking a task as complete updates its status."""
        task = self.task_service.add_task("Test Title")
        assert task.status == TaskStatus.INCOMPLETE

        completed_task = self.task_service.mark_task_complete(task.id)

        assert completed_task.status == TaskStatus.COMPLETE

    def test_mark_task_complete_returns_none_if_task_not_found(self):
        """Test that marking a non-existent task as complete returns None."""
        result = self.task_service.mark_task_complete("non-existent-id")

        assert result is None

    def test_mark_task_incomplete_marks_task_as_incomplete(self):
        """Test that marking a task as incomplete updates its status."""
        task = self.task_service.add_task("Test Title")
        # First mark as complete
        self.task_service.mark_task_complete(task.id)
        assert task.status == TaskStatus.COMPLETE

        incomplete_task = self.task_service.mark_task_incomplete(task.id)

        assert incomplete_task.status == TaskStatus.INCOMPLETE

    def test_mark_task_incomplete_returns_none_if_task_not_found(self):
        """Test that marking a non-existent task as incomplete returns None."""
        result = self.task_service.mark_task_incomplete("non-existent-id")

        assert result is None