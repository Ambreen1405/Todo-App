---
description: "Task list for Todo-CLI Agent implementation"
---

# Tasks: Todo-CLI Agent

**Input**: Design documents from `specs-history/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in src/
- [ ] T002 Initialize Python project with proper directory structure
- [ ] T003 [P] Create tests directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create Task entity model in src/entities/task.py
- [ ] T005 Create in-memory Task repository in src/interfaces/task_repository.py
- [ ] T006 Create Task service with business logic in src/use_cases/task_service.py
- [ ] T007 Create CLI argument parser in src/interfaces/cli_controller.py
- [ ] T008 Create main application entry point in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: User can add new tasks with title and optional description

**Independent Test**: User can run `todo add "Test task" "Optional description"` and see success message with assigned ID

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Unit test for Task entity creation in tests/unit/test_task.py
- [ ] T010 [P] [US1] Unit test for TaskService.add_task() in tests/unit/test_task_service.py
- [ ] T011 [P] [US1] Integration test for CLI add command in tests/integration/test_cli_add.py

### Implementation for User Story 1

- [ ] T012 [US1] Implement Task entity with id, title, description, status in src/entities/task.py
- [ ] T013 [US1] Implement add_task method in src/use_cases/task_service.py
- [ ] T014 [US1] Implement add command in CLI controller in src/interfaces/cli_controller.py
- [ ] T015 [US1] Integrate add command with main application in src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - List Tasks (Priority: P2)

**Goal**: User can list all tasks with their status

**Independent Test**: User can run `todo list` and see all tasks with ID, title, description, and completion status

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Unit test for TaskService.list_tasks() in tests/unit/test_task_service.py
- [ ] T017 [P] [US2] Integration test for CLI list command in tests/integration/test_cli_list.py

### Implementation for User Story 2

- [ ] T018 [US2] Implement list_tasks method in src/use_cases/task_service.py
- [ ] T019 [US2] Implement list command in CLI controller in src/interfaces/cli_controller.py
- [ ] T020 [US2] Integrate list command with main application in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P3)

**Goal**: User can update an existing task by ID

**Independent Test**: User can run `todo update 1 "New title" "New description"` and see success message

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T021 [P] [US3] Unit test for TaskService.update_task() in tests/unit/test_task_service.py
- [ ] T022 [P] [US3] Integration test for CLI update command in tests/integration/test_cli_update.py

### Implementation for User Story 3

- [ ] T023 [US3] Implement update_task method in src/use_cases/task_service.py
- [ ] T024 [US3] Implement update command in CLI controller in src/interfaces/cli_controller.py
- [ ] T025 [US3] Integrate update command with main application in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: User can delete a task by ID

**Independent Test**: User can run `todo delete 1` and see success message

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T026 [P] [US4] Unit test for TaskService.delete_task() in tests/unit/test_task_service.py
- [ ] T027 [P] [US4] Integration test for CLI delete command in tests/integration/test_cli_delete.py

### Implementation for User Story 4

- [ ] T028 [US4] Implement delete_task method in src/use_cases/task_service.py
- [ ] T029 [US4] Implement delete command in CLI controller in src/interfaces/cli_controller.py
- [ ] T030 [US4] Integrate delete command with main application in src/main.py

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P5)

**Goal**: User can mark tasks as complete or incomplete

**Independent Test**: User can run `todo complete 1` or `todo incomplete 1` and see success message

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US5] Unit test for TaskService.mark_complete/incomplete() in tests/unit/test_task_service.py
- [ ] T032 [P] [US5] Integration test for CLI complete/incomplete commands in tests/integration/test_cli_mark.py

### Implementation for User Story 5

- [ ] T033 [US5] Implement mark_complete and mark_incomplete methods in src/use_cases/task_service.py
- [ ] T034 [US5] Implement complete and incomplete commands in CLI controller in src/interfaces/cli_controller.py
- [ ] T035 [US5] Integrate complete/incomplete commands with main application in src/main.py

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T036 [P] Documentation updates in README.md
- [ ] T037 Code cleanup and refactoring
- [ ] T038 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T039 Error handling and validation across all commands
- [ ] T040 Run quickstart validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence