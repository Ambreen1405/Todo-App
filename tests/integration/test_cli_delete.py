"""
Integration tests for CLI delete command functionality.
"""
from io import StringIO
import sys
from unittest.mock import patch
import pytest
from src.interfaces.task_repository import TaskRepository
from src.use_cases.task_service import TaskService
from src.interfaces.cli_controller import CLIController


class TestCLIDeleteCommand:
    """Integration tests for the CLI delete command."""

    def setup_method(self):
        """Set up a fresh CLI controller for each test."""
        self.task_repository = TaskRepository()
        self.task_service = TaskService(self.task_repository)
        self.cli_controller = CLIController(self.task_service)

    def test_delete_command_removes_task(self):
        """Test that the delete command removes the specified task."""
        # Add a task first
        task = self.task_service.add_task("Test Title", "Test Description")

        # Verify task exists
        assert len(self.task_service.list_tasks()) == 1

        # Simulate command: todo delete <id>
        args = type('Args', (), {'id': task.id})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_delete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert f"Task {task.id} deleted successfully" in output

        # Verify the task was removed
        assert len(self.task_service.list_tasks()) == 0

    def test_delete_command_shows_error_for_nonexistent_task(self):
        """Test that the delete command shows an error for a non-existent task."""
        # Simulate command: todo delete "non-existent-id"
        args = type('Args', (), {'id': 'non-existent-id'})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_delete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command failed
        assert result == 1
        assert "Error: Task with ID non-existent-id not found" in output

    def test_delete_command_does_not_affect_other_tasks(self):
        """Test that deleting one task does not affect other tasks."""
        # Add multiple tasks
        task1 = self.task_service.add_task("Task 1", "Description 1")
        task2 = self.task_service.add_task("Task 2", "Description 2")
        task3 = self.task_service.add_task("Task 3", "Description 3")

        # Verify all tasks exist
        assert len(self.task_service.list_tasks()) == 3

        # Delete one task
        args = type('Args', (), {'id': task2.id})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_delete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert f"Task {task2.id} deleted successfully" in output

        # Verify only the specified task was removed
        remaining_tasks = self.task_service.list_tasks()
        assert len(remaining_tasks) == 2
        task_ids = [task.id for task in remaining_tasks]
        assert task1.id in task_ids
        assert task3.id in task_ids
        assert task2.id not in task_ids

    def test_delete_command_with_completed_task(self):
        """Test that the delete command works with completed tasks."""
        # Add and complete a task
        task = self.task_service.add_task("Test Title", "Test Description")
        self.task_service.mark_task_complete(task.id)
        assert task.status.value == "complete"

        # Verify task exists
        assert len(self.task_service.list_tasks()) == 1

        # Delete the task
        args = type('Args', (), {'id': task.id})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_delete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0

        # Verify the task was removed
        assert len(self.task_service.list_tasks()) == 0