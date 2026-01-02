"""
Integration tests for CLI update command functionality.
"""
from io import StringIO
import sys
from unittest.mock import patch
import pytest
from src.interfaces.task_repository import TaskRepository
from src.use_cases.task_service import TaskService
from src.interfaces.cli_controller import CLIController


class TestCLIUpdateCommand:
    """Integration tests for the CLI update command."""

    def setup_method(self):
        """Set up a fresh CLI controller for each test."""
        self.task_repository = TaskRepository()
        self.task_service = TaskService(self.task_repository)
        self.cli_controller = CLIController(self.task_service)

    def test_update_command_updates_task_title_and_description(self):
        """Test that the update command updates both title and description."""
        # Add a task first
        original_task = self.task_service.add_task("Original Title", "Original Description")

        # Simulate command: todo update <id> "New Title" "New Description"
        args = type('Args', (), {
            'id': original_task.id,
            'title': 'New Title',
            'description': 'New Description'
        })()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_update(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert f"Task {original_task.id} updated successfully" in output

        # Verify the task was updated
        updated_task = self.task_service.list_tasks()[0]
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_command_updates_title_only(self):
        """Test that the update command updates only the title when description is not provided."""
        # Add a task first
        original_task = self.task_service.add_task("Original Title", "Original Description")

        # Simulate command: todo update <id> "New Title" (no description)
        args = type('Args', (), {
            'id': original_task.id,
            'title': 'New Title',
            'description': None
        })()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_update(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert f"Task {original_task.id} updated successfully" in output

        # Verify the task was updated
        updated_task = self.task_service.list_tasks()[0]
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged

    def test_update_command_updates_description_only(self):
        """Test that the update command updates only the description when title is not provided."""
        # Add a task first
        original_task = self.task_service.add_task("Original Title", "Original Description")

        # Simulate command: todo update <id> (no title) "New Description"
        args = type('Args', (), {
            'id': original_task.id,
            'title': None,
            'description': 'New Description'
        })()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_update(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0
        assert f"Task {original_task.id} updated successfully" in output

        # Verify the task was updated
        updated_task = self.task_service.list_tasks()[0]
        assert updated_task.title == "Original Title"  # Should remain unchanged
        assert updated_task.description == "New Description"

    def test_update_command_shows_error_for_nonexistent_task(self):
        """Test that the update command shows an error for a non-existent task."""
        # Simulate command: todo update "non-existent-id" "New Title"
        args = type('Args', (), {
            'id': 'non-existent-id',
            'title': 'New Title',
            'description': 'New Description'
        })()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_update(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command failed
        assert result == 1
        assert "Error: Task with ID non-existent-id not found" in output

    def test_update_command_preserves_task_status(self):
        """Test that the update command preserves the task's status."""
        # Add and complete a task first
        original_task = self.task_service.add_task("Original Title", "Original Description")
        self.task_service.mark_task_complete(original_task.id)

        # Verify it's complete
        assert original_task.status.value == "complete"

        # Simulate command: todo update <id> "New Title"
        args = type('Args', (), {
            'id': original_task.id,
            'title': 'New Title',
            'description': None
        })()

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = self.cli_controller._handle_update(args)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verify the command was successful
        assert result == 0

        # Verify the task status is preserved
        updated_task = self.task_service.list_tasks()[0]
        assert updated_task.title == "New Title"
        assert updated_task.status.value == "complete"  # Should remain complete