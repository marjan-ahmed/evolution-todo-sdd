---
description: "Task list for Interactive CLI Todo Application implementation"
---

# Tasks: Interactive CLI Todo Application

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the feature specification, so test tasks are omitted. Focus on implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `phase-1-cli/src/phase_1_cli/`, `phase-1-cli/tests/` at repository root
- Paths shown assume single Python package structure with UV

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
- **User Story 1 only** (Add and View Tasks)
- This delivers immediate value as a task capture and display tool
- Validates architecture and core functionality
- Can be demonstrated and tested independently

### Incremental Delivery Plan
1. **Iteration 1**: US1 (Add + View) - Core MVP
2. **Iteration 2**: US2 (Toggle Status) - Progress tracking
3. **Iteration 3**: US3 (Update) + US4 (Delete) - Full CRUD
4. **Iteration 4**: US5 (Keyboard Navigation) - Polish

Each iteration delivers a working, demonstrable product increment.

---

## Dependencies Between User Stories

```
Setup (Phase 1) ──┐
                  ├──> Foundational (Phase 2) ──┐
                  │                              ├──> US1 ──> US2 ──> US3 ──> US4 ──> US5 ──> Polish
                  │                              │
                  └──────────────────────────────┘
```

**Dependency Rules**:
- **Setup** and **Foundational** phases MUST complete before any user story
- **US1** (Add + View) MUST complete first (establishes core architecture)
- **US2-US5** depend on US1 but can be partially parallelized after US1 is stable
- **Polish** phase touches all user stories (cross-cutting concerns)

**Parallel Opportunities**:
- Within Setup phase: Most tasks are parallelizable [P]
- Within Foundational phase: Models and services can be developed in parallel [P]
- Between user stories: After US1 stabilizes, US2-US5 can begin in parallel if multiple developers
- Within each user story: Screen implementations can be parallel [P]

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize Python project with UV and create directory structure per implementation plan.

**Tasks**:

- [ ] T001 Initialize UV package with `uv init --package phase-1-cli` at repository root
- [ ] T002 [P] Create directory structure: `phase-1-cli/src/phase_1_cli/{models,services,ui}/`
- [ ] T003 [P] Create directory structure: `phase-1-cli/tests/{unit,integration}/`
- [ ] T004 [P] Create empty __init__.py files in all package directories
- [ ] T005 Add core dependencies with `uv add textual rich pydantic`
- [ ] T006 [P] Add dev dependencies with `uv add --dev pytest pytest-asyncio`
- [ ] T007 [P] Create config.py in `phase-1-cli/src/phase_1_cli/config.py` with constants (icons, colors, limits)
- [ ] T008 [P] Create __main__.py entry point in `phase-1-cli/src/phase_1_cli/__main__.py`
- [ ] T009 Update pyproject.toml with project metadata and entry points
- [ ] T010 Verify installation with `uv run python -c "import textual; print(textual.__version__)"`

**Completion Criteria**:
- ✅ UV package initialized with proper structure
- ✅ All dependencies installed and importable
- ✅ Entry point configured (`uv run python -m phase_1_cli` runs without import errors)

---

## Phase 2: Foundational (Core Data and Business Logic)

**Purpose**: Implement data models and business logic that ALL user stories depend on.

**Independent Test**: After this phase, TaskManager can be imported and tested independently of any UI.

**Tasks**:

- [ ] T011 [P] Implement Task dataclass in `phase-1-cli/src/phase_1_cli/models/task.py` with fields: id, title, description, completed, created_at
- [ ] T012 [P] Implement TaskManager.__init__() in `phase-1-cli/src/phase_1_cli/services/task_manager.py` initializing tasks list and next_id counter
- [ ] T013 Implement TaskManager.add_task(title, description) method with validation and ID generation
- [ ] T014 [P] Implement TaskManager.get_task(task_id) method with linear search
- [ ] T015 [P] Implement TaskManager.update_task(task_id, title, description) method
- [ ] T016 [P] Implement TaskManager.delete_task(task_id) method
- [ ] T017 [P] Implement TaskManager.toggle_task(task_id) method
- [ ] T018 [P] Implement TaskManager.get_stats() method calculating total, pending, completed, percentage
- [ ] T019 Export Task and TaskManager in `phase-1-cli/src/phase_1_cli/models/__init__.py`
- [ ] T020 Export TaskManager in `phase-1-cli/src/phase_1_cli/services/__init__.py`

**Completion Criteria**:
- ✅ Task dataclass fully defined with all required fields
- ✅ TaskManager implements all CRUD operations
- ✅ TaskManager.get_stats() returns correct statistics
- ✅ All methods handle edge cases (empty lists, invalid IDs)
- ✅ Can create TaskManager instance and perform operations in Python REPL

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1)

**Goal**: Enable users to add tasks with titles/descriptions and view them in a styled table.

**Why First**: Core MVP. Establishes UI architecture, demonstrates visual polish, delivers immediate value.

**Independent Test**: After this phase, can launch app, add multiple tasks, see them in styled table with status indicators. App is usable as basic task capture tool.

**Tasks**:

### UI Foundation

- [ ] T021 [P] [US1] Create TodoApp class in `phase-1-cli/src/phase_1_cli/ui/app.py` extending Textual App
- [ ] T022 [P] [US1] Define Textual CSS in TodoApp for DataTable, stats panel, footer styling
- [ ] T023 [P] [US1] Define keyboard bindings in TodoApp: 'a' for add, 'q' for quit
- [ ] T024 [US1] Implement TodoApp.compose() method yielding Header, Stats widget, DataTable, Footer
- [ ] T025 [US1] Initialize TaskManager instance in TodoApp.__init__()

### Add Task Functionality

- [ ] T026 [P] [US1] Create AddTaskScreen modal in `phase-1-cli/src/phase_1_cli/ui/screens.py` with title and description input fields
- [ ] T027 [P] [US1] Style AddTaskScreen with Textual CSS (centered, bordered, proper spacing)
- [ ] T028 [US1] Implement AddTaskScreen.on_button_pressed() handler for Add/Cancel buttons
- [ ] T029 [US1] Implement TodoApp.action_add_task() to push AddTaskScreen and handle result
- [ ] T030 [US1] Add input validation in AddTaskScreen: reject empty titles, strip whitespace

### View Tasks Functionality

- [ ] T031 [US1] Implement TodoApp.on_mount() to initialize DataTable columns (ID, Status, Title, Description)
- [ ] T032 [US1] Implement TodoApp.refresh_table() method to populate DataTable from TaskManager.tasks
- [ ] T033 [US1] Implement TodoApp.refresh_stats() method to update stats panel from TaskManager.get_stats()
- [ ] T034 [US1] Add status icon rendering: ☐ for pending, ☑ for completed
- [ ] T035 [US1] Apply CSS classes to completed tasks (strike-through styling)
- [ ] T036 [US1] Handle empty state: display "No tasks yet. Press 'a' to add your first task!" when tasks list is empty

### Integration

- [ ] T037 [US1] Call refresh_table() and refresh_stats() after adding task
- [ ] T038 [US1] Update __main__.py to instantiate and run TodoApp
- [ ] T039 [US1] Verify app launches, add 3 tasks, see them in styled table with proper formatting

**Completion Criteria**:
- ✅ App launches without errors
- ✅ Can add tasks via 'a' keyboard shortcut or menu
- ✅ Tasks display in styled table with ID, Status (☐), Title, Description
- ✅ Statistics panel shows accurate counts and percentage
- ✅ Empty state displays friendly message
- ✅ Validation prevents empty titles
- ✅ Can quit with 'q' key

---

## Phase 4: User Story 2 - Toggle Task Status (Priority: P2)

**Goal**: Enable users to mark tasks complete/incomplete with immediate visual feedback.

**Why Second**: Adds progress tracking capability, showcases responsiveness principle.

**Independent Test**: After this phase, can add tasks, toggle their status with spacebar, see status icons change (☐ ↔ ☑), statistics update in real-time.

**Dependencies**: Requires US1 (Add and View) to be complete.

**Tasks**:

- [ ] T040 [P] [US2] Add keyboard binding for 'space' key to TodoApp.BINDINGS
- [ ] T041 [US2] Implement TodoApp.action_toggle_task() method to get selected row and call TaskManager.toggle_task()
- [ ] T042 [US2] Handle case when no task is selected: display error message in status bar or modal
- [ ] T043 [US2] Update refresh_table() to apply 'completed' CSS class for completed tasks (strike-through text)
- [ ] T044 [US2] Call refresh_table() and refresh_stats() after toggling task status
- [ ] T045 [US2] Add visual feedback: flash row or show brief confirmation message on toggle
- [ ] T046 [US2] Verify toggle works: add task, press space, see ☐ → ☑, stats update, press space again, see ☑ → ☐

**Completion Criteria**:
- ✅ Spacebar toggles selected task completion status
- ✅ Status icon changes immediately (☐ ↔ ☑)
- ✅ Statistics update in real-time
- ✅ Completed tasks show strike-through styling
- ✅ Toggle works bidirectionally (complete → incomplete → complete)
- ✅ Error handling for no selection case

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable users to edit task titles and descriptions.

**Why Third**: Adds refinement capability, prevents frustration from typos.

**Independent Test**: After this phase, can create task with typo, edit it via 'e' key, update title/description, see changes reflected in table.

**Dependencies**: Requires US1 (Add and View) to be complete.

**Tasks**:

- [ ] T047 [P] [US3] Add keyboard binding for 'e' key to TodoApp.BINDINGS
- [ ] T048 [P] [US3] Create EditTaskScreen modal in `phase-1-cli/src/phase_1_cli/ui/screens.py` pre-populated with task data
- [ ] T049 [P] [US3] Style EditTaskScreen similar to AddTaskScreen with Save/Cancel buttons
- [ ] T050 [US3] Implement TodoApp.action_edit_task() to get selected task and push EditTaskScreen
- [ ] T051 [US3] Handle case when no task is selected: display error "No task selected. Select a task first."
- [ ] T052 [US3] Implement EditTaskScreen.on_mount() to pre-fill input fields with current task data
- [ ] T053 [US3] Implement EditTaskScreen.on_button_pressed() to call TaskManager.update_task() on Save
- [ ] T054 [US3] Add validation: reject empty titles in EditTaskScreen
- [ ] T055 [US3] Call refresh_table() after updating task
- [ ] T056 [US3] Verify editing works: create task "Review PR", edit to "Review PR #345", see change in table

**Completion Criteria**:
- ✅ 'e' key opens edit modal for selected task
- ✅ Modal pre-fills with current task data
- ✅ Can update title and/or description
- ✅ Validation prevents empty titles
- ✅ Changes reflect immediately in table
- ✅ Cancel button discards changes
- ✅ Error handling for no selection

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable users to delete tasks with confirmation dialog.

**Why Fourth**: Adds list management capability, demonstrates good UX practices.

**Independent Test**: After this phase, can create test task, press 'd', see confirmation dialog, confirm deletion, task removed from list.

**Dependencies**: Requires US1 (Add and View) to be complete.

**Tasks**:

- [ ] T057 [P] [US4] Add keyboard binding for 'd' key to TodoApp.BINDINGS
- [ ] T058 [P] [US4] Create ConfirmDialog modal in `phase-1-cli/src/phase_1_cli/ui/screens.py` with title, message, Confirm/Cancel buttons
- [ ] T059 [P] [US4] Style ConfirmDialog with error/warning color scheme (red border)
- [ ] T060 [US4] Implement TodoApp.action_delete_task() to get selected task and show confirmation
- [ ] T061 [US4] Handle case when no task is selected: display error "No task selected"
- [ ] T062 [US4] Implement ConfirmDialog to display task title in confirmation message: "Delete 'Task title'?"
- [ ] T063 [US4] Call TaskManager.delete_task() only if user confirms (not on cancel)
- [ ] T064 [US4] Call refresh_table() and refresh_stats() after deletion
- [ ] T065 [US4] Display success message: "Task deleted successfully"
- [ ] T066 [US4] Verify deletion: add task, press 'd', cancel first time (task remains), press 'd' again, confirm (task removed)

**Completion Criteria**:
- ✅ 'd' key shows confirmation dialog for selected task
- ✅ Dialog displays task title in message
- ✅ Confirm button deletes task
- ✅ Cancel button preserves task
- ✅ Task removed from table after confirmation
- ✅ Statistics update after deletion
- ✅ Success feedback shown
- ✅ Error handling for no selection

---

## Phase 7: User Story 5 - Keyboard-Driven Navigation (Priority: P5)

**Goal**: Display keyboard shortcuts in footer and ensure all operations keyboard-accessible.

**Why Fifth**: Polish feature that elevates user experience from good to excellent.

**Independent Test**: After this phase, can perform all operations (add, edit, delete, toggle) using only keyboard, footer shows available shortcuts.

**Dependencies**: Requires US1-US4 to be complete (all operations must exist).

**Tasks**:

- [ ] T067 [US5] Update all keyboard bindings in TodoApp.BINDINGS with `show=True` for primary actions
- [ ] T068 [US5] Set `key_display` parameter for special keys: "/" for search (future), "?" for help (future)
- [ ] T069 [US5] Verify Footer widget displays all keyboard shortcuts automatically from BINDINGS
- [ ] T070 [US5] Customize Footer styling with Textual CSS for better readability
- [ ] T071 [US5] Add arrow key navigation: ensure DataTable cursor_type="row" for keyboard navigation
- [ ] T072 [US5] Test full keyboard workflow: launch app, press 'a', add task, press down arrow, press space (toggle), press 'e', edit task, press 'd', delete task, press 'q' (quit) - all without mouse
- [ ] T073 [US5] Verify Escape key closes all modals (AddTaskScreen, EditTaskScreen, ConfirmDialog)

**Completion Criteria**:
- ✅ Footer displays: "a=Add | e=Edit | d=Delete | space=Toggle | q=Quit"
- ✅ All operations accessible via keyboard only
- ✅ Arrow keys navigate task list
- ✅ Enter key works for modal confirmations
- ✅ Escape key cancels/closes modals
- ✅ Can complete full workflow without mouse
- ✅ Shortcuts are discoverable (visible in footer)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Handle edge cases, add error handling, ensure constitutional compliance.

**Dependencies**: Requires all user stories (US1-US5) to be complete.

**Tasks**:

### Edge Case Handling

- [ ] T074 [P] Handle terminal too small: check terminal size on startup, display warning if <80x24, exit gracefully
- [ ] T075 [P] Handle long titles (500+ chars): truncate display in table at 100 chars with ellipsis, store full text
- [ ] T076 [P] Handle long descriptions: truncate display at 500 chars, show full text in detail view (future enhancement)
- [ ] T077 [P] Handle special characters and emojis: verify UTF-8 encoding displays correctly across platforms
- [ ] T078 [P] Handle non-numeric ID input: add input validation in EditTaskScreen and ConfirmDialog for task ID selection
- [ ] T079 [P] Handle rapid task additions: verify no race conditions, IDs remain unique, performance stays under 1 second for 100 tasks

### Error Messages and Validation

- [ ] T080 [P] Standardize error message format: use consistent style and color (red) for all error messages
- [ ] T081 [P] Add comprehensive input validation messages: "Title is required", "Task not found", "Invalid task ID"
- [ ] T082 [P] Test all validation rules: empty titles, invalid IDs, non-existent tasks

### Cross-Platform Testing

- [ ] T083 Verify app runs on Windows 10/11: test terminal colors, keyboard shortcuts, character encoding
- [ ] T084 Verify app runs on macOS 12+: test terminal colors, keyboard shortcuts, character encoding
- [ ] T085 Verify app runs on Ubuntu 20.04+: test terminal colors, keyboard shortcuts, character encoding

### Performance Validation

- [ ] T086 Performance test with 100 tasks: add 100 tasks, verify operations complete in <1 second, UI updates in <200ms
- [ ] T087 Stress test with 1000 tasks: add 1000 tasks, verify no crashes, acceptable performance degradation

### Documentation

- [ ] T088 [P] Update README.md in `phase-1-cli/` with usage instructions, keyboard shortcuts, installation guide
- [ ] T089 [P] Add docstrings to all public methods in TaskManager and TodoApp
- [ ] T090 [P] Create examples in README showing common workflows

### Final Validation

- [ ] T091 Verify all success criteria from spec.md: SC-001 through SC-010
- [ ] T092 Verify all constitutional principles satisfied: Intuitive UX, Aesthetic Design, Modular Architecture, Reusability, Responsiveness, Cross-Platform
- [ ] T093 Run full manual test suite: add, view, toggle, edit, delete operations with edge cases
- [ ] T094 Record demo video showing all features for hackathon presentation

**Completion Criteria**:
- ✅ All edge cases handled gracefully
- ✅ Error messages are clear and actionable
- ✅ Cross-platform compatibility verified
- ✅ Performance targets met (SC-005, SC-006)
- ✅ All success criteria validated
- ✅ Documentation complete
- ✅ Ready for demo/presentation

---

## Summary

**Total Tasks**: 94
**Parallel Opportunities**: 34 tasks marked with [P]

### Tasks Per User Story

| Phase | Story | Task Count | Can Start After |
|-------|-------|------------|-----------------|
| Phase 1 | Setup | 10 | - |
| Phase 2 | Foundational | 10 | Phase 1 |
| Phase 3 | US1 (Add + View) | 19 | Phase 2 |
| Phase 4 | US2 (Toggle Status) | 7 | Phase 3 |
| Phase 5 | US3 (Update Details) | 10 | Phase 3 |
| Phase 6 | US4 (Delete Tasks) | 10 | Phase 3 |
| Phase 7 | US5 (Keyboard Nav) | 7 | Phases 4-6 |
| Phase 8 | Polish | 21 | Phase 7 |

### Parallel Execution Examples

**Within US1 (after T025 completes)**:
- T026, T027 (AddTaskScreen) in parallel
- T031, T032 (DataTable setup) in parallel

**Between User Stories (after US1 stabilizes)**:
- US2 (T040-T046) can start
- US3 (T047-T056) can start in parallel with US2
- US4 (T057-T066) can start in parallel with US2 and US3

**Within Polish Phase**:
- T074-T082 (edge cases and validation) all parallel
- T088-T090 (documentation) all parallel

### Independent Test Criteria

- **After Phase 2**: TaskManager works in Python REPL
- **After Phase 3 (US1)**: Can add and view tasks in styled table
- **After Phase 4 (US2)**: Can toggle task status with visual feedback
- **After Phase 5 (US3)**: Can edit existing tasks
- **After Phase 6 (US4)**: Can delete tasks with confirmation
- **After Phase 7 (US5)**: Can perform all operations via keyboard only
- **After Phase 8**: Production-ready application meeting all success criteria

### Suggested MVP Scope

**Minimum Viable Product = Phase 1 + Phase 2 + Phase 3 (US1 only)**

This delivers:
- Working task capture tool
- Visual polish (styled table, status indicators)
- Basic statistics display
- Demonstrates core architecture
- Can be demoed and evaluated

**Total MVP Tasks**: 39 tasks (Phases 1-3)
**Estimated MVP Completion**: ~40% of total work, but delivers 80% of core value
