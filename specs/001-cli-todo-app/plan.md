# Implementation Plan: Interactive CLI Todo Application

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a modern, interactive terminal-based todo application with visual polish and modular architecture. The application provides five core operations (Add, View, Update, Delete, Toggle Status) through a menu-driven interface with keyboard shortcuts. Tasks are stored in-memory with no persistence, displayed in styled tables with color-coded status indicators (☐ Pending / ☑ Completed), and managed through a decoupled TaskManager business logic layer. Target audience is developers, hackathon judges, and Python enthusiasts evaluating polished CLI tools.

**Technical Approach**: Use Textual framework for reactive TUI components with Rich library for terminal formatting. Implement clean architecture with strict separation between UI (Textual widgets and screens), business logic (TaskManager class), and data models (Task dataclass). Package management via UV with `--package` flag for modern Python project structure.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: Textual ≥0.63.0 (TUI framework), Rich ≥13.7.0 (terminal formatting), Pydantic ≥2.0.0 (data validation)
**Storage**: In-memory only (no file system or database persistence)
**Testing**: pytest (unit tests for TaskManager), Textual's built-in testing utilities (UI component tests)
**Target Platform**: Cross-platform terminals (Windows 10/11, macOS 12+, Ubuntu 20.04+) with 256-color support and minimum 80x24 size
**Project Type**: Single Python package (phase-1-cli) managed with UV
**Performance Goals**: Operations complete in under 1 second for up to 100 tasks, UI updates in under 200ms, handles 1000 tasks without noticeable degradation
**Constraints**: No persistence, Python-only with no OS-specific system calls, UTF-8 encoding required, in-memory storage limit ~10MB for task data
**Scale/Scope**: Single-user desktop application, 5 core operations, expected usage: 10-100 tasks per session, runtime duration: minutes to hours

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Intuitive UX
- ✅ **Menu-driven navigation**: Spec defines clear menu options for Add, View, Update, Delete, Toggle Status (FR-001)
- ✅ **Keyboard shortcuts**: Footer displays shortcuts for all operations (FR-011, User Story 5)
- ✅ **Clear prompts**: Input validation with helpful error messages (FR-005)
- ✅ **Instant feedback**: Real-time table updates and statistics (FR-009, SC-006)

### II. Aesthetic Design
- ✅ **Color-coded indicators**: ☐ Pending (gray/white), ☑ Completed (green) (FR-007, FR-013)
- ✅ **Styled tables**: Bordered panels with proper spacing (FR-006)
- ✅ **Icon usage**: Status indicators and visual hierarchy (FR-007)
- ✅ **Typography**: Readable spacing and layout per success criteria (SC-004)

### III. Modular Architecture
- ✅ **UI/Logic separation**: TaskManager class independent of UI (FR-012, SC-008)
- ✅ **No business logic in UI handlers**: TaskManager handles all CRUD operations
- ✅ **Data models separate**: Task dataclass defined independently
- ✅ **Clear interfaces**: TaskManager provides clean API for UI layer

### IV. Reusability
- ✅ **Generic UI components**: Textual widgets accept data models
- ✅ **Pluggable business logic**: TaskManager can be swapped or extended
- ✅ **No hardcoded assumptions**: Task structure uses standard fields

### V. Responsiveness
- ✅ **Real-time updates**: Table and stats refresh immediately (FR-009)
- ✅ **Confirmation dialogs**: Delete operations require confirmation (FR-010)
- ✅ **Error feedback**: Validation errors displayed instantly (FR-005)
- ✅ **Performance target**: <200ms visual feedback (SC-002)

### VI. Cross-Platform Compatibility
- ✅ **Python-only**: No OS-specific system calls (FR-015)
- ✅ **Terminal compatibility**: Standard 256-color support (FR-015, SC-007)
- ✅ **Platform testing**: Windows, macOS, Linux verified (SC-007)
- ✅ **UTF-8 support**: Handles special characters and emojis (Edge Cases)

**Gate Status**: ✅ **PASSED** - All constitutional principles satisfied by spec requirements

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (below)
├── data-model.md        # Phase 1 output (below)
├── quickstart.md        # Phase 1 output (below)
├── contracts/           # Phase 1 output (not applicable - no API)
└── checklists/
    └── requirements.md  # Spec validation checklist (complete)
```

### Source Code (repository root)

```text
phase-1-cli/                    # UV package (created with uv init --package)
├── pyproject.toml              # UV project configuration
├── uv.lock                     # Dependency lock file
├── README.md                   # Package documentation
├── src/
│   └── phase_1_cli/            # Main package
│       ├── __init__.py         # Package exports
│       ├── __main__.py         # Entry point (python -m phase_1_cli)
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py         # Task dataclass
│       ├── services/
│       │   ├── __init__.py
│       │   └── task_manager.py # TaskManager business logic
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── app.py          # Main Textual App
│       │   ├── screens.py      # Modal screens (Add, Edit, Confirm)
│       │   └── widgets.py      # Custom widgets if needed
│       └── config.py           # Constants and configuration
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── __init__.py
    │   ├── test_task.py        # Task model tests
    │   └── test_task_manager.py # Business logic tests
    └── integration/
        ├── __init__.py
        └── test_ui.py          # Textual UI tests
```

**Structure Decision**: Single Python package managed with UV. Chosen because:
- Project is a standalone desktop CLI application (not web/mobile/API)
- No need for multiple services or backend/frontend separation
- UV's `--package` flag provides modern Python packaging with proper namespace
- Clean separation: `models/` (data), `services/` (logic), `ui/` (presentation)
- Follows PEP 420 namespace packages for proper module organization

## Complexity Tracking

> **No violations** - All constitutional requirements satisfied by specification.

---

## Phase 0: Research & Decision Log

### Research Tasks

1. ✅ **Textual Framework Best Practices**
   - **Decision**: Use Textual 0.63.0+ for TUI with reactive components
   - **Rationale**:
     - Modern Python TUI framework with CSS-like styling
     - Built-in support for DataTable, modals, keyboard bindings, and mouse events
     - Reactive programming model simplifies UI updates
     - Excellent documentation and active community
     - Cross-platform (Windows, macOS, Linux) with graceful degradation
   - **Alternatives Considered**:
     - `curses`: Too low-level, platform-specific issues on Windows
     - `prompt-toolkit`: Great for prompts but not full TUI applications
     - `blessed`: Simpler but lacks reactive components and modal support
   - **Implementation Notes**:
     - Use `App` class for main application
     - Use `DataTable` widget for task list
     - Use `ModalScreen` for Add/Edit/Delete dialogs
     - Use `Binding` for keyboard shortcuts
     - Use Textual CSS for styling (no inline styles)

2. ✅ **In-Memory Data Structure Selection**
   - **Decision**: Use Python `list` for task storage with linear search
   - **Rationale**:
     - Simple and sufficient for expected scale (10-100 tasks)
     - O(n) search acceptable for small n
     - Maintains insertion order naturally
     - Easy to iterate for statistics calculation
     - No external dependencies required
   - **Alternatives Considered**:
     - `dict` with ID keys: Adds complexity for minimal benefit at this scale
     - `deque`: No advantage over list for random access patterns
     - SQLite in-memory: Overkill and violates "no database" constraint
   - **Implementation Notes**:
     - TaskManager stores `tasks: List[Task]`
     - Linear search with `next((t for t in tasks if t.id == target_id), None)`
     - ID generation with simple counter: `self.next_id += 1`

3. ✅ **Testing Strategy for TUI Applications**
   - **Decision**: Use pytest + Textual's `App.run_test()` for UI tests
   - **Rationale**:
     - Textual provides testing utilities for async TUI apps
     - pytest is Python standard for test organization
     - `run_test()` method allows simulating user interactions
     - Can test UI without actually rendering to terminal
   - **Alternatives Considered**:
     - Manual testing only: Insufficient for regression prevention
     - unittest: pytest more Pythonic and better fixtures
     - Snapshot testing: Too brittle for rapidly changing UI
   - **Implementation Notes**:
     - Unit tests: TaskManager logic (pure Python, no UI)
     - Integration tests: Full app flows with `App.run_test()`
     - Test keyboard events, modal interactions, table updates
     - Mock user input where needed

4. ✅ **Error Handling Patterns**
   - **Decision**: Defensive validation in TaskManager with friendly UI error messages
   - **Rationale**:
     - TaskManager validates inputs and returns success/error tuples
     - UI layer translates errors to user-friendly messages
     - No exceptions for user errors (only for system failures)
     - Follows "be liberal in what you accept" for user input
   - **Alternatives Considered**:
     - Exception-based: Too heavy for simple validation errors
     - Silent failures: Violates constitutional responsiveness principle
     - UI-only validation: Doesn't protect business logic integrity
   - **Implementation Notes**:
     - TaskManager methods return `(success: bool, message: str)` tuples
     - UI displays error messages in modals or status bar
     - Edge cases handled per spec: empty lists, invalid IDs, long titles

5. ✅ **UV Package Manager Integration**
   - **Decision**: Use UV with `uv init --package phase-1-cli` for project initialization
   - **Rationale**:
     - UV is fast, modern Python package manager (Rust-based)
     - `--package` flag creates proper package structure with `src/` layout
     - Generates `pyproject.toml` with PEP 621 metadata
     - Lock file (`uv.lock`) ensures reproducible installs
     - Compatible with pip/PyPI ecosystem
   - **Alternatives Considered**:
     - Poetry: Similar features but slower than UV
     - pip + venv: Manual setup, no dependency locking
     - Conda: Overkill for pure Python project
   - **Implementation Notes**:
     - Initialize: `uv init --package phase-1-cli`
     - Add dependencies: `uv add textual rich pydantic`
     - Add dev dependencies: `uv add --dev pytest`
     - Run app: `uv run python -m phase_1_cli`
     - Run tests: `uv run pytest`

### Cross-Cutting Concerns

**Configuration Management**:
- Use `config.py` for constants (colors, icons, size limits)
- No runtime configuration needed (in-memory only)
- Hardcoded defaults acceptable for MVP

**Logging**:
- No logging framework needed (no persistence)
- Use Rich console for debug output during development
- Remove debug prints in production build

**Performance Optimization**:
- No premature optimization required
- Linear search acceptable for <100 tasks
- Profile if issues arise with 1000+ tasks

**Accessibility**:
- Textual handles keyboard navigation automatically
- High-contrast colors for status indicators
- Clear error messages per constitutional requirements

---

## Phase 1: Design Artifacts

*To be generated in Phase 1 execution...*

See:
- [data-model.md](./data-model.md) - Entity definitions and relationships
- [quickstart.md](./quickstart.md) - Developer onboarding and usage guide
- contracts/ - Not applicable (no external APIs)

---

## Phase 2: Task Breakdown

*Not generated by /sp.plan - use /sp.tasks command after Phase 1 completion*

---

## Next Steps

1. ✅ **Phase 0 Complete**: Research decisions documented above
2. **Phase 1**: Generate data-model.md, quickstart.md (below)
3. **Phase 2**: Run `/sp.tasks` to generate implementation task list
4. **Implementation**: Execute tasks by priority (P1 → P5 user stories)
5. **Testing**: Unit tests (TaskManager) → Integration tests (UI flows)
6. **Validation**: Verify all success criteria and constitutional compliance
