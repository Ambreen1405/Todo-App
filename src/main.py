

"""
Main entry point for the Todo CLI application.
"""
from src.interfaces.task_repository import TaskRepository
from src.use_cases.task_service import TaskService
from src.interfaces.cli_controller import CLIController
import sys


def main():
    """Main entry point for the application."""
    # Initialize the application components
    task_repository = TaskRepository()
    task_service = TaskService(task_repository)
    cli_controller = CLIController(task_service)

    # Handle the command line arguments
    exit_code = cli_controller.handle_command()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()