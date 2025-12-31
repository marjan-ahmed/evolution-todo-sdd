# Textual Patterns Reference

Common patterns for building Textual applications.

## Table of Contents
- Reactive Variables
- Widgets and Containers
- Styling with CSS
- Event Handling
- Modal Screens
- Data Binding

## Reactive Variables

Update UI automatically when data changes:

```python
from textual.reactive import reactive

class TodoApp(App):
    task_count = reactive(0)

    def watch_task_count(self, old_value: int, new_value: int) -> None:
        """Called automatically when task_count changes"""
        self.query_one("#stats").update(f"Total: {new_value}")
```

## Core Widgets

### DataTable
```python
from textual.widgets import DataTable

table = self.query_one(DataTable)
table.add_columns("ID", "Title", "Status")
table.add_row("1", "Buy milk", "☐ Pending")
table.zebra_stripes = True

# Handle row selection
def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
    row_key = event.row_key
    # Process selection
```

### Input Fields
```python
from textual.widgets import Input

class AddTaskScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Task title", id="title")
        yield Input(placeholder="Description", id="description")
        yield Button("Add", variant="success")

    def on_button_pressed(self) -> None:
        title = self.query_one("#title", Input).value
        description = self.query_one("#description", Input).value
        self.dismiss({"title": title, "description": description})
```

### Buttons
```python
from textual.widgets import Button

# Variants: default, primary, success, warning, error
Button("Save", variant="success", id="save")
Button("Cancel", variant="default", id="cancel")
Button("Delete", variant="error", id="delete")
```

## Container Layouts

### Horizontal
```python
from textual.containers import Horizontal

Horizontal(
    Button("Left"),
    Button("Middle"),
    Button("Right"),
)
```

### Vertical
```python
from textual.containers import Vertical

Vertical(
    Static("Header"),
    DataTable(),
    Static("Footer"),
)
```

### Grid
```python
from textual.containers import Grid

Grid(
    Static("A"), Static("B"),
    Static("C"), Static("D"),
)

# In CSS
Grid {
    grid-size: 2 2;
    grid-gutter: 1;
}
```

## Styling with Textual CSS

```python
class TodoApp(App):
    CSS = """
    Screen {
        background: $surface;
    }

    DataTable {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }

    #stats {
        height: 3;
        background: $panel;
        color: $text;
        text-align: center;
    }

    .completed {
        text-style: strike;
        color: $success;
    }

    Button {
        margin: 1;
        min-width: 16;
    }

    Button.success {
        background: $success;
    }

    Input {
        border: solid $accent;
        padding: 1;
    }

    Input:focus {
        border: solid $primary;
    }
    """
```

### CSS Variables
- `$primary`, `$secondary`, `$accent` - Theme colors
- `$success`, `$warning`, `$error` - Status colors
- `$surface`, `$panel` - Background colors
- `$text`, `$text-muted` - Text colors

### Layout Properties
- `height: 1fr` - Take available space
- `height: auto` - Fit content
- `height: 10` - Fixed rows
- `width: 100%` - Full width
- `padding: 1` - Inner spacing
- `margin: 1` - Outer spacing

## Event Handling

### Key Events
```python
from textual import events

def on_key(self, event: events.Key) -> None:
    if event.key == "escape":
        self.pop_screen()
    elif event.key == "enter":
        self.submit_form()
```

### Widget Events
```python
def on_button_pressed(self, event: Button.Pressed) -> None:
    if event.button.id == "add":
        self.add_task()

def on_input_changed(self, event: Input.Changed) -> None:
    self.filter_tasks(event.value)

def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
    self.selected_row = event.row_key
```

## Modal Screens

```python
from textual.screen import ModalScreen

class AddTaskScreen(ModalScreen[dict]):
    """Modal for adding new task"""

    CSS = """
    AddTaskScreen {
        align: center middle;
    }

    #dialog {
        width: 60;
        height: auto;
        border: solid $primary;
        background: $surface;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static("Add New Task", classes="title")
            yield Input(placeholder="Title", id="title")
            yield Input(placeholder="Description", id="description")
            yield Horizontal(
                Button("Add", variant="success", id="add"),
                Button("Cancel", variant="default", id="cancel")
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            title = self.query_one("#title", Input).value
            desc = self.query_one("#description", Input).value
            self.dismiss({"title": title, "description": desc})
        else:
            self.dismiss(None)

# Usage
def action_add_task(self) -> None:
    def handle_result(result: dict | None) -> None:
        if result:
            self.task_manager.add_task(result["title"], result["description"])
            self.refresh_table()

    self.push_screen(AddTaskScreen(), handle_result)
```

## Data Binding to DataTable

```python
def refresh_table(self) -> None:
    """Update table with current tasks"""
    table = self.query_one(DataTable)
    table.clear()

    for task in self.task_manager.tasks:
        status = "☑" if task.completed else "☐"
        style = "completed" if task.completed else ""

        table.add_row(
            str(task.id),
            status,
            task.title,
            task.description,
            key=str(task.id),
            classes=style
        )

    # Update stats
    stats = self.task_manager.get_stats()
    self.query_one("#stats").update(
        f"Total: {stats['total']} | "
        f"Pending: {stats['pending']} | "
        f"Completed: {stats['completed']} | "
        f"Progress: {stats['percentage']:.1f}%"
    )
```

## Keyboard Bindings

```python
from textual.binding import Binding

class TodoApp(App):
    BINDINGS = [
        Binding("a", "add_task", "Add Task"),
        Binding("d", "delete_task", "Delete", show=True),
        Binding("e", "edit_task", "Edit"),
        Binding("space", "toggle_task", "Toggle"),
        Binding("ctrl+s", "save", "Save", show=False),
        Binding("q", "quit", "Quit"),
    ]

    def action_add_task(self) -> None:
        self.push_screen(AddTaskScreen())

    def action_delete_task(self) -> None:
        # Delete selected task
        pass
```

## Loading and Startup

```python
def on_mount(self) -> None:
    """Called when app is mounted"""
    table = self.query_one(DataTable)
    table.add_columns("ID", "Status", "Title", "Description")
    table.cursor_type = "row"
    table.zebra_stripes = True

    # Load initial data
    self.refresh_table()

    # Set focus
    table.focus()
```

## Rich Integration

```python
from rich.console import Console
from rich.table import Table as RichTable

# Use Rich for exports
def export_to_markdown(self) -> str:
    console = Console(record=True)
    table = RichTable(title="Tasks")

    table.add_column("ID")
    table.add_column("Status")
    table.add_column("Title")

    for task in self.task_manager.tasks:
        table.add_row(
            str(task.id),
            "☑" if task.completed else "☐",
            task.title
        )

    console.print(table)
    return console.export_text()
```
