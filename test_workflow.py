"""
Test script to verify all CLI functionality works together in one execution.
"""
from src.interfaces.task_repository import TaskRepository
from src.use_cases.task_service import TaskService
from src.interfaces.cli_controller import CLIController


def test_full_workflow():
    """Test the full workflow of the todo app."""
    # Initialize the application components
    task_repository = TaskRepository()
    task_service = TaskService(task_repository)
    cli_controller = CLIController(task_service)

    print("=== Testing Add Task ===")
    # Simulate adding a task
    import sys
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    # Add a task
    result = cli_controller._handle_add(type('Args', (), {'title': 'Test Task', 'description': 'Test Description'})())
    output = captured_output.getvalue()
    sys.stdout = old_stdout
    print(output.strip())

    print("\n=== Testing List Tasks ===")
    # Capture list output
    sys.stdout = captured_output = StringIO()
    result = cli_controller._handle_list()
    output = captured_output.getvalue()
    sys.stdout = old_stdout
    print(output.strip())

    print("\n=== Testing Update Task ===")
    # Get the first task ID to update
    tasks = task_service.list_tasks()
    if tasks:
        task_id = tasks[0].id
        # Update the task
        sys.stdout = captured_output = StringIO()
        result = cli_controller._handle_update(type('Args', (), {'id': task_id, 'title': 'Updated Task', 'description': 'Updated Description'})())
        output = captured_output.getvalue()
        sys.stdout = old_stdout
        print(output.strip())

        print("\n=== Testing List After Update ===")
        # List again to see the update
        sys.stdout = captured_output = StringIO()
        result = cli_controller._handle_list()
        output = captured_output.getvalue()
        sys.stdout = old_stdout
        print(output.strip())

        print("\n=== Testing Mark Complete ===")
        # Mark as complete
        sys.stdout = captured_output = StringIO()
        result = cli_controller._handle_complete(type('Args', (), {'id': task_id})())
        output = captured_output.getvalue()
        sys.stdout = old_stdout
        print(output.strip())

        print("\n=== Testing List After Complete ===")
        # List again to see the status change
        sys.stdout = captured_output = StringIO()
        result = cli_controller._handle_list()
        output = captured_output.getvalue()
        sys.stdout = old_stdout
        print(output.strip())

        print("\n=== Testing Delete Task ===")
        # Delete the task
        sys.stdout = captured_output = StringIO()
        result = cli_controller._handle_delete(type('Args', (), {'id': task_id})())
        output = captured_output.getvalue()
        sys.stdout = old_stdout
        print(output.strip())

        print("\n=== Testing List After Delete ===")
        # List again to see that task is gone
        sys.stdout = captured_output = StringIO()
        result = cli_controller._handle_list()
        output = captured_output.getvalue()
        sys.stdout = old_stdout
        print(output.strip())


if __name__ == "__main__":
    test_full_workflow()