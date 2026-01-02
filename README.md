



# Todo-CLI Agent

A command-line interface (CLI) application for managing todo tasks with in-memory storage.

## Features

- Add tasks with title and optional description
- List all tasks with their status
- Update tasks by ID
- Delete tasks by ID
- Mark tasks as complete/incomplete

## Requirements

- Python 3.13 or higher

## Installation

No installation required - this is a Python script that can be run directly.

## Usage

### Add a task

```bash
python -m src.main add "Task title" "Optional description"
```

Example:
```bash
python -m src.main add "Buy groceries" "Milk, bread, eggs"
```

### List all tasks

```bash
python -m src.main list
```

### Update a task

```bash
python -m src.main update <task_id> "New title" "Optional new description"
```

Example:
```bash
python -m src.main update 123e4567-e89b-12d3-a456-426614174000 "Updated title" "Updated description"
```

### Delete a task

```bash
python -m src.main delete <task_id>
```

Example:
```bash
python -m src.main delete 123e4567-e89b-12d3-a456-426614174000
```

### Mark a task as complete

```bash
python -m src.main complete <task_id>
```

### Mark a task as incomplete

```bash
python -m src.main incomplete <task_id>
```

## Architecture

The application follows clean architecture principles:

- **Entities** (`src/entities/`): Domain entities (Task model)
- **Use Cases** (`src/use_cases/`): Business logic (TaskService)
- **Interfaces** (`src/interfaces/`): Interface adapters (CLI controller)
- **Main** (`src/main.py`): Application entry point

## Data Storage

The application uses in-memory storage only. Tasks are not persisted between application runs.

## Project Structure

```
src/
├── entities/              # Domain entities (Task model)
├── use_cases/             # Business logic (TaskService)
├── interfaces/            # Interface adapters (CLI controller)
└── main.py                # Entry point for the CLI application

tests/
├── unit/                  # Unit tests for entities and use cases
├── integration/           # Integration tests for CLI functionality
└── conftest.py            # Test configuration
```

## Testing

Run all tests:

```bash
python -m pytest tests/
```

Run specific test file:

```bash
python -m pytest tests/unit/test_task.py
```# Todo-App
