"""
Integration tests for CLI complete/incomplete command functionality.
"""
from io import StringIO
import sys
from unittest.mock import patch
import pytest
from src.interfaces.task_repository import TaskRepository
from src.use_cases.task_service import TaskService
from src.interfaces.cli_controller import CLIController


class TestCLIMarkCommands:
    """Integration tests for the CLI complete/incomplete commands."""

    def setup_method(self):
        """Set up a fresh CLI controller for each test."""
        self.task_repository = TaskRepository()
        self.task_service = TaskService(self.task_repository)
        self.cli_controller = CLIController(self.task_service)

    def test_complete_command_marks_task_as_complete(self):
        """Test that the complete command marks a task as complete."""
        # Add a task first (should be incomplete by default)
        task = self.task_service.add_task("Test Title", "Test Description")
        assert task.status.value == "incomplete"

        # Simulate command: todo complete <id>
        args = type('Args', (), {'id': task.id})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_complete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert f"Task {task.id} marked as complete" in output

        # Verify the task status was updated
        updated_task = self.task_repository.get_by_id(task.id)
        assert updated_task.status.value == "complete"

    def test_incomplete_command_marks_task_as_incomplete(self):
        """Test that the incomplete command marks a task as incomplete."""
        # Add and complete a task
        task = self.task_service.add_task("Test Title", "Test Description")
        self.task_service.mark_task_complete(task.id)
        assert task.status.value == "complete"

        # Simulate command: todo incomplete <id>
        args = type('Args', (), {'id': task.id})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_incomplete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert f"Task {task.id} marked as incomplete" in output

        # Verify the task status was updated
        updated_task = self.task_repository.get_by_id(task.id)
        assert updated_task.status.value == "incomplete"

    def test_complete_command_shows_error_for_nonexistent_task(self):
        """Test that the complete command shows an error for a non-existent task."""
        # Simulate command: todo complete "non-existent-id"
        args = type('Args', (), {'id': 'non-existent-id'})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_complete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command failed
        assert result == 1
        assert "Error: Task with ID non-existent-id not found" in output

    def test_incomplete_command_shows_error_for_nonexistent_task(self):
        """Test that the incomplete command shows an error for a non-existent task."""
        # Simulate command: todo incomplete "non-existent-id"
        args = type('Args', (), {'id': 'non-existent-id'})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_incomplete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command failed
        assert result == 1
        assert "Error: Task with ID non-existent-id not found" in output

    def test_complete_command_on_already_completed_task(self):
        """Test that the complete command works on an already completed task."""
        # Add and complete a task
        task = self.task_service.add_task("Test Title", "Test Description")
        self.task_service.mark_task_complete(task.id)
        assert task.status.value == "complete"

        # Try to mark it complete again
        args = type('Args', (), {'id': task.id})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_complete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert f"Task {task.id} marked as complete" in output

        # Verify the task status is still complete
        updated_task = self.task_repository.get_by_id(task.id)
        assert updated_task.status.value == "complete"

    def test_incomplete_command_on_already_incomplete_task(self):
        """Test that the incomplete command works on an already incomplete task."""
        # Add a task (should be incomplete by default)
        task = self.task_service.add_task("Test Title", "Test Description")
        assert task.status.value == "incomplete"

        # Try to mark it incomplete again
        args = type('Args', (), {'id': task.id})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_incomplete(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert f"Task {task.id} marked as incomplete" in output

        # Verify the task status is still incomplete
        updated_task = self.task_repository.get_by_id(task.id)
        assert updated_task.status.value == "incomplete"