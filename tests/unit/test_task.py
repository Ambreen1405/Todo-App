"""
Unit tests for the Task entity.
"""
import pytest
from src.entities.task import Task, TaskStatus


class TestTask:
    """Test cases for the Task entity."""

    def test_task_creation_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(id="1", title="Test Task", description="Test Description", status=TaskStatus.INCOMPLETE)
        assert task.id == "1"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == TaskStatus.INCOMPLETE

    def test_task_creation_defaults(self):
        """Test creating a task with default values."""
        task = Task(id="1", title="Test Task")
        assert task.id == "1"
        assert task.title == "Test Task"
        assert task.description is None
        assert task.status == TaskStatus.INCOMPLETE

    def test_task_creation_without_id_raises_error(self):
        """Test that creating a task without an ID raises an error."""
        with pytest.raises(ValueError):
            Task(id="", title="Test Task")

    def test_task_creation_without_title_raises_error(self):
        """Test that creating a task without a title raises an error."""
        with pytest.raises(ValueError):
            Task(id="1", title="")

    def test_mark_complete_changes_status(self):
        """Test that marking a task as complete changes its status."""
        task = Task(id="1", title="Test Task", status=TaskStatus.INCOMPLETE)
        task.mark_complete()
        assert task.status == TaskStatus.COMPLETE

    def test_mark_incomplete_changes_status(self):
        """Test that marking a task as incomplete changes its status."""
        task = Task(id="1", title="Test Task", status=TaskStatus.COMPLETE)
        task.mark_incomplete()
        assert task.status == TaskStatus.INCOMPLETE

    def test_to_dict_returns_correct_format(self):
        """Test that to_dict returns the correct dictionary format."""
        task = Task(id="1", title="Test Task", description="Test Description", status=TaskStatus.COMPLETE)
        expected_dict = {
            "id": "1",
            "title": "Test Task",
            "description": "Test Description",
            "status": "complete"
        }
        assert task.to_dict() == expected_dict