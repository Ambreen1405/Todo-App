"""
CLI controller for handling command-line interface operations.
"""
import argparse
from typing import Optional
from src.use_cases.task_service import TaskService
from src.entities.task import Task


class CLIController:
    """Controller for CLI operations."""

    def __init__(self, task_service: TaskService):
        """Initialize the CLI controller with a task service."""
        self.task_service = task_service
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser with all available commands."""
        parser = argparse.ArgumentParser(
            prog='todo',
            description='Todo CLI Application',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Add command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('title', help='Title of the task')
        add_parser.add_argument('description', nargs='?', default=None, help='Description of the task (optional)')

        # List command
        list_parser = subparsers.add_parser('list', help='List all tasks')

        # Update command
        update_parser = subparsers.add_parser('update', help='Update an existing task')
        update_parser.add_argument('id', help='ID of the task to update')
        update_parser.add_argument('title', nargs='?', default=None, help='New title of the task (optional)')
        update_parser.add_argument('description', nargs='?', default=None, help='New description of the task (optional)')

        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('id', help='ID of the task to delete')

        # Complete command
        complete_parser = subparsers.add_parser('complete', help='Mark a task as complete')
        complete_parser.add_argument('id', help='ID of the task to mark complete')

        # Incomplete command
        incomplete_parser = subparsers.add_parser('incomplete', help='Mark a task as incomplete')
        incomplete_parser.add_argument('id', help='ID of the task to mark incomplete')

        return parser

    def handle_command(self, args=None):
        """Handle the command based on parsed arguments."""
        parsed_args = self.parser.parse_args(args)

        if parsed_args.command == 'add':
            return self._handle_add(parsed_args)
        elif parsed_args.command == 'list':
            return self._handle_list()
        elif parsed_args.command == 'update':
            return self._handle_update(parsed_args)
        elif parsed_args.command == 'delete':
            return self._handle_delete(parsed_args)
        elif parsed_args.command == 'complete':
            return self._handle_complete(parsed_args)
        elif parsed_args.command == 'incomplete':
            return self._handle_incomplete(parsed_args)
        else:
            self.parser.print_help()
            return 0

    def _handle_add(self, args) -> int:
        """Handle the add command."""
        try:
            task = self.task_service.add_task(args.title, args.description)
            print(f"Task added successfully with ID: {task.id}")
            return 0
        except ValueError as e:
            print(f"Error: {e}")
            return 1

    def _handle_list(self) -> int:
        """Handle the list command."""
        tasks = self.task_service.list_tasks()
        if not tasks:
            print("No tasks found.")
            return 0

        print(f"{'ID':<36} {'Status':<10} {'Title':<30} {'Description'}")
        print("-" * 80)
        for task in tasks:
            status = "DONE" if task.status.value == "complete" else "TODO"
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            description = task.description or ""
            if len(description) > 30:
                description = description[:27] + "..."
            print(f"{task.id:<36} {status:<10} {title:<30} {description}")
        return 0

    def _handle_update(self, args) -> int:
        """Handle the update command."""
        try:
            task = self.task_service.update_task(args.id, args.title, args.description)
            if task:
                print(f"Task {args.id} updated successfully")
                return 0
            else:
                print(f"Error: Task with ID {args.id} not found")
                return 1
        except ValueError as e:
            print(f"Error: {e}")
            return 1

    def _handle_delete(self, args) -> int:
        """Handle the delete command."""
        success = self.task_service.delete_task(args.id)
        if success:
            print(f"Task {args.id} deleted successfully")
            return 0
        else:
            print(f"Error: Task with ID {args.id} not found")
            return 1

    def _handle_complete(self, args) -> int:
        """Handle the complete command."""
        task = self.task_service.mark_task_complete(args.id)
        if task:
            print(f"Task {args.id} marked as complete")
            return 0
        else:
            print(f"Error: Task with ID {args.id} not found")
            return 1

    def _handle_incomplete(self, args) -> int:
        """Handle the incomplete command."""
        task = self.task_service.mark_task_incomplete(args.id)
        if task:
            print(f"Task {args.id} marked as incomplete")
            return 0
        else:
            print(f"Error: Task with ID {args.id} not found")
            return 1