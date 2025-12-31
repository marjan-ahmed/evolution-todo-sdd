# Quick Start Guide: Interactive CLI Todo Application

**Feature**: Interactive CLI Todo Application
**Branch**: `001-cli-todo-app`
**Created**: 2025-12-31

## Prerequisites

- Python 3.8 or higher
- UV package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Terminal with 256-color support and UTF-8 encoding
- Minimum terminal size: 80 columns × 24 rows

## Project Setup

### 1. Initialize the Project

```bash
# Create the project with UV
uv init --package phase-1-cli
cd phase-1-cli
```

This creates the following structure:
```
phase-1-cli/
├── pyproject.toml
├── README.md
└── src/
    └── phase_1_cli/
        └── __init__.py
```

### 2. Install Dependencies

```bash
# Add core dependencies
uv add textual rich pydantic

# Add development dependencies
uv add --dev pytest pytest-asyncio

# Verify installation
uv run python -c "import textual; print(textual.__version__)"
```

### 3. Project Structure

Create the following directory structure:

```bash
mkdir -p src/phase_1_cli/{models,services,ui}
mkdir -p tests/{unit,integration}
touch src/phase_1_cli/{__main__.py,config.py}
touch src/phase_1_cli/models/{__init__.py,task.py}
touch src/phase_1_cli/services/{__init__.py,task_manager.py}
touch src/phase_1_cli/ui/{__init__.py,app.py,screens.py,widgets.py}
touch tests/{__init__.py,unit/{__init__.py,test_task.py,test_task_manager.py}}
touch tests/integration/{__init__.py,test_ui.py}
```

Final structure:
```
phase-1-cli/
├── pyproject.toml
├── uv.lock
├── README.md
├── src/
│   └── phase_1_cli/
│       ├── __init__.py
│       ├── __main__.py          # Entry point
│       ├── config.py             # Constants
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py          # Task dataclass
│       ├── services/
│       │   ├── __init__.py
│       │   └── task_manager.py  # Business logic
│       └── ui/
│           ├── __init__.py
│           ├── app.py           # Main Textual app
│           ├── screens.py       # Modal screens
│           └── widgets.py       # Custom widgets
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── __init__.py
    │   ├── test_task.py
    │   └── test_task_manager.py
    └── integration/
        ├── __init__.py
        └── test_ui.py
```

## Running the Application

### Development Mode

```bash
# Run the application
uv run python -m phase_1_cli

# Or with UV's run command
uv run phase-1-cli
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=phase_1_cli --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_task_manager.py

# Run with verbose output
uv run pytest -v

# Run only unit tests
uv run pytest tests/unit/

# Run only integration tests
uv run pytest tests/integration/
```

### Linting and Formatting

```bash
# Add development tools
uv add --dev ruff mypy

# Run linter
uv run ruff check src/ tests/

# Format code
uv run ruff format src/ tests/

# Type checking
uv run mypy src/
```

## Usage Examples

### Basic Workflow

1. **Launch the application**:
   ```bash
   uv run python -m phase_1_cli
   ```

2. **Add a task** (Press `a` or select "Add Task"):
   - Enter title: "Fix bug in auth module"
   - Enter description: "Memory leak in token validation"
   - Press Enter to confirm

3. **View tasks** (automatically displayed):
   - Tasks appear in styled table with ID, Status, Title, Description
   - Statistics shown at top: Total, Pending, Completed, Progress %

4. **Toggle task status** (Press `space` or select "Toggle Status"):
   - Select task with arrow keys
   - Press spacebar to mark complete/incomplete
   - Status changes from ☐ to ☑ (or vice versa)

5. **Edit a task** (Press `e` or select "Edit Task"):
   - Enter task ID
   - Update title and/or description
   - Press Enter to save

6. **Delete a task** (Press `d` or select "Delete Task"):
   - Enter task ID
   - Confirm deletion in dialog
   - Task removed from list

7. **Quit** (Press `q` or select "Quit"):
   - Application exits gracefully

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `a` | Add new task |
| `e` | Edit selected task |
| `d` | Delete selected task |
| `space` | Toggle task completion |
| `↑`/`↓` | Navigate task list |
| `Enter` | Select/Confirm |
| `Esc` | Cancel/Close modal |
| `q` | Quit application |
| `?` | Show help (future enhancement) |

## Development Workflow

### 1. Implement Data Layer

Start with the data model (simplest, no dependencies):

```bash
# Edit src/phase_1_cli/models/task.py
# Implement Task dataclass

# Test it
uv run pytest tests/unit/test_task.py -v
```

### 2. Implement Business Logic

Next, implement TaskManager (depends on Task):

```bash
# Edit src/phase_1_cli/services/task_manager.py
# Implement TaskManager class

# Test it
uv run pytest tests/unit/test_task_manager.py -v
```

### 3. Implement UI Layer

Finally, build the Textual UI:

```bash
# Edit src/phase_1_cli/ui/app.py
# Implement TodoApp

# Edit src/phase_1_cli/ui/screens.py
# Implement modal screens (AddTaskScreen, EditTaskScreen, ConfirmDialog)

# Edit src/phase_1_cli/__main__.py
# Add entry point

# Test manually
uv run python -m phase_1_cli
```

### 4. Add Integration Tests

```bash
# Edit tests/integration/test_ui.py
# Test full workflows with Textual's run_test()

uv run pytest tests/integration/ -v
```

## Configuration

Edit `src/phase_1_cli/config.py` for constants:

```python
# config.py
from typing import Final

# UI Constants
MIN_TERMINAL_WIDTH: Final[int] = 80
MIN_TERMINAL_HEIGHT: Final[int] = 24

# Display Limits
MAX_TITLE_DISPLAY_LENGTH: Final[int] = 100
MAX_DESCRIPTION_DISPLAY_LENGTH: Final[int] = 500

# Status Icons
ICON_PENDING: Final[str] = "☐"
ICON_COMPLETED: Final[str] = "☑"

# Colors (Textual CSS color names)
COLOR_PENDING: Final[str] = "$text"
COLOR_COMPLETED: Final[str] = "$success"
COLOR_BORDER: Final[str] = "$primary"

# Statistics
STATS_FORMAT: Final[str] = (
    "📊 Total: {total} | ⏳ Pending: {pending} | "
    "✅ Completed: {completed} | 📈 Progress: {percentage:.1f}%"
)
```

## Troubleshooting

### UV Not Found
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

### Terminal Too Small
```bash
# Resize terminal to at least 80x24
# On Linux/macOS: resize
# On Windows: drag window or set properties
```

### Import Errors
```bash
# Reinstall dependencies
uv sync

# Or clean and reinstall
rm -rf .venv uv.lock
uv sync
```

### Textual Not Rendering Colors
```bash
# Check terminal color support
echo $TERM  # Should be xterm-256color or similar

# Force 256-color mode
export TERM=xterm-256color
```

### Tests Failing
```bash
# Run with verbose output
uv run pytest -vv

# Run specific test
uv run pytest tests/unit/test_task_manager.py::test_add_task -v

# Check Python version
python --version  # Should be 3.8+
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         User Input                          │
│                    (Keyboard/Mouse Events)                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      UI Layer (Textual)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   TodoApp   │  │   Screens    │  │     Widgets      │   │
│  │  (main app) │  │ (Add, Edit,  │  │  (DataTable,     │   │
│  │             │  │  Delete)     │  │   Static, etc.)  │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ (calls methods)
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                 Business Logic Layer                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              TaskManager                            │   │
│  │  - add_task()                                       │   │
│  │  - get_task()                                       │   │
│  │  - update_task()                                    │   │
│  │  - delete_task()                                    │   │
│  │  - toggle_task()                                    │   │
│  │  - get_stats()                                      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ (manages collection)
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Task (dataclass)                       │   │
│  │  - id: int                                          │   │
│  │  - title: str                                       │   │
│  │  - description: str                                 │   │
│  │  - completed: bool                                  │   │
│  │  - created_at: datetime                             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Key Principles**:
- **Unidirectional data flow**: UI → TaskManager → Task
- **No business logic in UI**: All CRUD operations in TaskManager
- **UI is replaceable**: Could swap Textual for curses, web, etc.
- **Business logic is testable**: TaskManager has no UI dependencies

## Next Steps

1. **Implement Phase 1** (Core MVP):
   - Add and View Tasks (User Story P1)
   - Basic table display with status indicators
   - In-memory storage with TaskManager

2. **Implement Phase 2** (Progress Tracking):
   - Toggle Task Status (User Story P2)
   - Real-time statistics
   - Visual feedback for status changes

3. **Implement Phase 3** (Editing):
   - Update Task Details (User Story P3)
   - Edit modal with validation

4. **Implement Phase 4** (Deletion):
   - Delete Tasks (User Story P4)
   - Confirmation dialog

5. **Implement Phase 5** (Polish):
   - Keyboard-Driven Navigation (User Story P5)
   - Footer with keyboard hints
   - Edge case handling

6. **Testing & Validation**:
   - Unit tests for all TaskManager methods
   - Integration tests for user workflows
   - Verify success criteria (SC-001 through SC-010)
   - Cross-platform testing (Windows, macOS, Linux)

## References

- [Textual Documentation](https://textual.textualize.io/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Data Model](./data-model.md)
