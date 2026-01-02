"""
Integration tests for CLI add command functionality.
"""
from io import StringIO
import sys
from unittest.mock import patch
import pytest
from src.interfaces.task_repository import TaskRepository
from src.use_cases.task_service import TaskService
from src.interfaces.cli_controller import CLIController


class TestCLIAddCommand:
    """Integration tests for the CLI add command."""

    def setup_method(self):
        """Set up a fresh CLI controller for each test."""
        self.task_repository = TaskRepository()
        self.task_service = TaskService(self.task_repository)
        self.cli_controller = CLIController(self.task_service)

    def test_add_command_creates_task_with_title_and_description(self):
        """Test that the add command creates a task with provided title and description."""
        # Simulate command: todo add "Test Title" "Test Description"
        args = type('Args', (), {'title': 'Test Title', 'description': 'Test Description'})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_add(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert "Task added successfully" in output
        assert len(self.task_service.list_tasks()) == 1

        # Verify the task was created with correct properties
        task = self.task_service.list_tasks()[0]
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.status.value == "incomplete"

    def test_add_command_creates_task_with_title_only(self):
        """Test that the add command creates a task with only a title."""
        # Simulate command: todo add "Test Title"
        args = type('Args', (), {'title': 'Test Title', 'description': None})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_add(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert "Task added successfully" in output
        assert len(self.task_service.list_tasks()) == 1

        # Verify the task was created with correct properties
        task = self.task_service.list_tasks()[0]
        assert task.title == "Test Title"
        assert task.description is None
        assert task.status.value == "incomplete"

    def test_add_command_with_invalid_title_shows_error(self):
        """Test that the add command shows an error with an invalid title."""
        # Simulate command: todo add "" (empty title)
        args = type('Args', (), {'title': '', 'description': 'Test Description'})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_add(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command failed
        assert result == 1
        assert "Error:" in output
        assert len(self.task_service.list_tasks()) == 0

    def test_add_command_shows_generated_task_id(self):
        """Test that the add command shows the generated task ID."""
        # Simulate command: todo add "Test Title"
        args = type('Args', (), {'title': 'Test Title', 'description': 'Test Description'})()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_add(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful and shows an ID
        assert result == 0
        assert "Task added successfully" in output
        assert "Task added successfully with ID:" in output

        # Extract the ID from the output
        output_lines = output.strip().split('\n')
        task_id_line = [line for line in output_lines if "Task added successfully with ID:" in line][0]
        task_id = task_id_line.split("Task added successfully with ID: ")[1].strip()

        # Verify the ID is a valid UUID string
        assert len(task_id) > 0
        assert task_id in [task.id for task in self.task_service.list_tasks()]