"""
Integration tests for CLI list command functionality.
"""
from io import StringIO
import sys
from unittest.mock import patch
import pytest
from src.interfaces.task_repository import TaskRepository
from src.use_cases.task_service import TaskService
from src.interfaces.cli_controller import CLIController


class TestCLIListCommand:
    """Integration tests for the CLI list command."""

    def setup_method(self):
        """Set up a fresh CLI controller for each test."""
        self.task_repository = TaskRepository()
        self.task_service = TaskService(self.task_repository)
        self.cli_controller = CLIController(self.task_service)

    def test_list_command_shows_no_tasks_when_empty(self):
        """Test that the list command shows 'No tasks found' when there are no tasks."""
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_list()
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful and shows no tasks
        assert result == 0
        assert "No tasks found." in output

    def test_list_command_shows_single_task(self):
        """Test that the list command shows a single task correctly."""
        # Add a task first
        task = self.task_service.add_task("Test Title", "Test Description")

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_list()
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert task.id in output
        assert "Test Title" in output
        assert "Test Description" in output
        assert "TODO" in output  # Should show as incomplete

    def test_list_command_shows_multiple_tasks(self):
        """Test that the list command shows multiple tasks correctly."""
        # Add multiple tasks
        task1 = self.task_service.add_task("Task 1", "Description 1")
        task2 = self.task_service.add_task("Task 2", "Description 2")
        task3 = self.task_service.add_task("Task 3")  # No description

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_list()
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful and shows all tasks
        assert result == 0
        assert task1.id in output
        assert task2.id in output
        assert task3.id in output
        assert "Task 1" in output
        assert "Task 2" in output
        assert "Task 3" in output
        assert "Description 1" in output
        assert "Description 2" in output

    def test_list_command_shows_completed_tasks_correctly(self):
        """Test that the list command shows completed tasks with correct status."""
        # Add and complete a task
        task = self.task_service.add_task("Test Title", "Test Description")
        self.task_service.mark_task_complete(task.id)

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_list()
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful and shows task as complete
        assert result == 0
        assert task.id in output
        assert "Test Title" in output
        assert "DONE" in output  # Should show as complete

    def test_list_command_formatting(self):
        """Test that the list command has proper formatting."""
        # Add a task
        task = self.task_service.add_task("Test Title", "Test Description")

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_list()
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful and has proper formatting
        assert result == 0

        lines = output.strip().split('\n')
        # Should have header line and separator
        assert "ID" in lines[0]
        assert "Status" in lines[0]
        assert "Title" in lines[0]
        assert "Description" in lines[0]
        assert "-" in lines[1]  # Separator line