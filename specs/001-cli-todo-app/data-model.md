# Data Model: Interactive CLI Todo Application

**Feature**: Interactive CLI Todo Application
**Branch**: `001-cli-todo-app`
**Created**: 2025-12-31

## Overview

This document defines the data structures for the in-memory todo application. The model consists of two primary components: the `Task` entity representing individual todo items, and the `TaskManager` service managing the task collection.

## Entities

### Task

Represents a single todo item with metadata and completion status.

**Fields**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `int` | Yes | Auto-generated | Unique identifier, auto-incremented starting from 1 |
| `title` | `str` | Yes | - | Brief description of what needs to be done (max display: 100 chars) |
| `description` | `str` | No | `""` | Additional details or context (max display: 500 chars) |
| `completed` | `bool` | Yes | `False` | Status indicating if task is done |
| `created_at` | `datetime` | Yes | Auto-generated | Timestamp of task creation (UTC) |

**Validation Rules**:
- `title` MUST NOT be empty string after stripping whitespace
- `title` length SHOULD be reasonable (truncate display at 100 chars, accept up to 500)
- `description` can be empty but SHOULD truncate display at 500 chars if longer
- `id` MUST be unique within the TaskManager collection
- `id` MUST be positive integer
- `created_at` is immutable after creation

**State Transitions**:
```
[Created] ──toggle──> [Completed]
    ▲                      │
    └───────toggle─────────┘
```

**Implementation Notes**:
- Use Python `dataclass` with `@dataclass` decorator
- `created_at` uses `field(default_factory=datetime.now)`
- No persistence layer - exists only in memory during runtime
- ID assignment happens in TaskManager, not in Task constructor

**Example**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

---

### TaskManager

Business logic service managing the task collection with CRUD operations and statistics.

**Purpose**: Encapsulates all task business logic separately from UI layer, enabling reusability and testability.

**State**:

| Field | Type | Description |
|-------|------|-------------|
| `tasks` | `List[Task]` | In-memory collection of all tasks |
| `next_id` | `int` | Counter for generating unique task IDs |

**Operations**:

#### add_task(title: str, description: str = "") → Task
Creates and adds a new task to the collection.

**Pre-conditions**:
- `title` must not be empty after stripping whitespace

**Post-conditions**:
- New task added to `tasks` list
- `next_id` incremented
- Task has unique ID
- Task has current timestamp

**Returns**: The newly created `Task` object

**Validation**:
- Strip whitespace from title and description
- Reject if title is empty
- Truncate title/description if exceeds reasonable limits (implementation detail)

---

#### get_task(task_id: int) → Task | None
Retrieves a task by its ID.

**Pre-conditions**:
- `task_id` is a positive integer

**Returns**:
- `Task` object if found
- `None` if not found

**Implementation**: Linear search through `tasks` list

---

#### update_task(task_id: int, title: str | None = None, description: str | None = None) → bool
Updates task fields by ID.

**Pre-conditions**:
- Task with `task_id` exists
- If `title` provided, must not be empty after stripping

**Post-conditions**:
- Specified fields updated on task
- `created_at` and `id` remain unchanged

**Returns**:
- `True` if update successful
- `False` if task not found or validation fails

---

#### delete_task(task_id: int) → bool
Removes a task from the collection.

**Pre-conditions**:
- Task with `task_id` exists

**Post-conditions**:
- Task removed from `tasks` list
- No gaps in remaining IDs (IDs are never reused)

**Returns**:
- `True` if deletion successful
- `False` if task not found

---

#### toggle_task(task_id: int) → bool
Toggles the completion status of a task.

**Pre-conditions**:
- Task with `task_id` exists

**Post-conditions**:
- Task's `completed` status flipped: `False` → `True` or `True` → `False`

**Returns**:
- `True` if toggle successful
- `False` if task not found

---

#### get_stats() → dict
Calculates statistics for all tasks.

**Returns**: Dictionary with keys:
- `total` (int): Total number of tasks
- `completed` (int): Number of completed tasks
- `pending` (int): Number of pending tasks
- `percentage` (float): Completion percentage (0.0-100.0)

**Calculation**:
- `completed` = count of tasks where `completed == True`
- `pending` = `total - completed`
- `percentage` = `(completed / total * 100)` if `total > 0` else `0.0`

---

## Relationships

```
TaskManager (1) ──manages──> (*) Task
```

- One TaskManager instance manages multiple Task instances
- Tasks have no references to TaskManager (unidirectional)
- Tasks are independent entities (no parent-child relationships between tasks)
- No cascade delete (only TaskManager holds task references)

## Data Flow

### Creating a Task
1. UI layer calls `TaskManager.add_task(title, description)`
2. TaskManager validates title (not empty)
3. TaskManager creates Task with `next_id`
4. TaskManager increments `next_id`
5. TaskManager appends Task to `tasks` list
6. TaskManager returns Task object
7. UI layer displays updated task list

### Updating Task Status
1. UI layer calls `TaskManager.toggle_task(task_id)`
2. TaskManager finds task by ID (linear search)
3. TaskManager flips `completed` boolean
4. TaskManager returns success status
5. UI layer refreshes table and statistics

### Deleting a Task
1. UI layer calls `TaskManager.delete_task(task_id)`
2. TaskManager finds task by ID
3. TaskManager removes task from list
4. TaskManager returns success status
5. UI layer refreshes table and statistics

## Invariants

The following must ALWAYS be true:

1. **Unique IDs**: No two tasks have the same ID
2. **Positive IDs**: All task IDs are positive integers (>= 1)
3. **Monotonic IDs**: `next_id` always increases, never decreases
4. **Valid Titles**: No task has an empty title
5. **Immutable Creation Time**: `created_at` never changes after task creation
6. **Immutable IDs**: Task IDs never change after creation

## Performance Characteristics

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| add_task | O(1) | O(1) | Append to list |
| get_task | O(n) | O(1) | Linear search |
| update_task | O(n) | O(1) | Linear search + update |
| delete_task | O(n) | O(1) | Linear search + remove |
| toggle_task | O(n) | O(1) | Linear search + update |
| get_stats | O(n) | O(1) | Full list iteration |

**Justification for O(n) operations**:
- Expected task count: 10-100 (typical usage)
- Linear search acceptable for this scale
- Simpler implementation than dict-based lookup
- No premature optimization needed

## Edge Cases

### Empty Collection
- `get_stats()` returns `{"total": 0, "completed": 0, "pending": 0, "percentage": 0.0}`
- `get_task()` always returns `None`
- `update_task()`, `delete_task()`, `toggle_task()` always return `False`

### Long Titles/Descriptions
- UI layer truncates display (not data model responsibility)
- Data model accepts strings up to Python's string limit
- Recommendation: UI validates length before calling TaskManager

### Rapid Task Creation
- IDs continue incrementing (no overflow risk for reasonable usage)
- Python int has unlimited precision (no 32-bit overflow)
- Memory limit: ~10MB for 10,000 tasks (rough estimate)

### Invalid IDs
- Negative or zero IDs never returned by TaskManager
- UI layer validates numeric input before calling operations
- `get_task(invalid_id)` returns `None` (safe handling)

## Memory Footprint Estimate

Per task (approximate):
- `id`: 28 bytes (Python int object)
- `title`: 50 bytes (string, average length)
- `description`: 100 bytes (string, average length)
- `completed`: 28 bytes (Python bool object)
- `created_at`: 48 bytes (datetime object)
- Overhead: 50 bytes (object, pointers)

**Total per task**: ~304 bytes

**Capacity estimates**:
- 100 tasks: ~30 KB
- 1,000 tasks: ~300 KB
- 10,000 tasks: ~3 MB

All well within memory constraints for a desktop CLI application.

## Testing Considerations

### Unit Tests (TaskManager)
- Test ID generation (uniqueness, incrementing)
- Test validation (empty titles rejected)
- Test CRUD operations (all success and failure paths)
- Test statistics calculation (empty, partial, full completion)
- Test edge cases (invalid IDs, non-existent tasks)

### Property-Based Tests
- Invariants hold after any sequence of operations
- IDs always unique
- Statistics always sum correctly

### Performance Tests
- Measure operations with 100, 1000, 10000 tasks
- Verify no degradation under success criteria (<1 second for 100 tasks)

## Migration Notes

**N/A** - No persistence, no migrations. Data exists only in memory during application runtime.
