# UI/UX Features Reference

Comprehensive UI enhancements for terminal todo apps.

## Table of Contents
- Status Indicators
- Progress Bars
- Live Search and Filtering
- Tabs and Views
- Confirmation Dialogs
- Stats Dashboard
- Animations and Transitions
- Theme Support
- Bulk Operations

## Status Indicators

### Visual Status Icons
```python
STATUS_ICONS = {
    "pending": "☐",
    "completed": "☑",
    "in_progress": "⏳",
    "cancelled": "❌"
}

PRIORITY_ICONS = {
    "high": "🔴",
    "medium": "🟡",
    "low": "🟢"
}

# Usage in table
status_icon = STATUS_ICONS[task.status]
priority_icon = PRIORITY_ICONS[task.priority]
table.add_row(f"{priority_icon} {status_icon}", task.title)
```

### Color Coding
```python
CSS = """
.pending {
    color: $text-muted;
}

.completed {
    color: $success;
    text-style: strike;
}

.high-priority {
    color: $error;
    text-style: bold;
}

.medium-priority {
    color: $warning;
}

.low-priority {
    color: $success;
}
"""
```

## Progress Bars

### Overall Progress
```python
from textual.widgets import ProgressBar

class TodoApp(App):
    def compose(self) -> ComposeResult:
        yield ProgressBar(total=100, id="progress")

    def update_progress(self) -> None:
        stats = self.task_manager.get_stats()
        progress = self.query_one("#progress", ProgressBar)
        progress.update(progress=stats['percentage'])
```

### Rich Progress Bars
```python
from rich.progress import Progress, BarColumn, TextColumn

def show_stats_with_progress(self) -> None:
    stats = self.task_manager.get_stats()

    with Progress() as progress:
        task = progress.add_task(
            "[green]Completion",
            total=stats['total'],
            completed=stats['completed']
        )
```

## Live Search and Filtering

### Real-time Search
```python
from textual.widgets import Input

class TodoApp(App):
    search_term = reactive("")

    def compose(self) -> ComposeResult:
        yield Input(placeholder="🔍 Search tasks...", id="search")
        yield DataTable()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.search_term = event.value
        self.refresh_table()

    def refresh_table(self) -> None:
        table = self.query_one(DataTable)
        table.clear()

        filtered_tasks = [
            t for t in self.task_manager.tasks
            if self.search_term.lower() in t.title.lower()
            or self.search_term.lower() in t.description.lower()
        ]

        for task in filtered_tasks:
            table.add_row(task.id, task.title, task.description)
```

### Filter by Status
```python
from textual.widgets import RadioSet, RadioButton

class TodoApp(App):
    filter_mode = reactive("all")

    def compose(self) -> ComposeResult:
        yield RadioSet(
            RadioButton("All", id="all"),
            RadioButton("Active", id="active"),
            RadioButton("Completed", id="completed"),
        )
        yield DataTable()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.filter_mode = event.pressed.id
        self.refresh_table()

    def get_filtered_tasks(self) -> list:
        if self.filter_mode == "active":
            return [t for t in self.task_manager.tasks if not t.completed]
        elif self.filter_mode == "completed":
            return [t for t in self.task_manager.tasks if t.completed]
        return self.task_manager.tasks
```

## Tabs and Views

### Tabbed Interface
```python
from textual.widgets import TabbedContent, TabPane

class TodoApp(App):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("All", id="all"):
                yield DataTable(id="table-all")
            with TabPane("Active", id="active"):
                yield DataTable(id="table-active")
            with TabPane("Completed", id="completed"):
                yield DataTable(id="table-completed")

    def on_tabbed_content_tab_activated(self, event) -> None:
        # Refresh active tab's table
        self.refresh_table(event.pane.id)
```

### Split View Layout
```python
from textual.containers import Horizontal, Vertical

class TodoApp(App):
    CSS = """
    #left-panel {
        width: 60%;
    }

    #right-panel {
        width: 40%;
        border-left: solid $primary;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="left-panel"):
                yield Static("Task List")
                yield DataTable()
            with Vertical(id="right-panel"):
                yield Static("Task Details")
                yield Static(id="task-details")

    def on_data_table_row_selected(self, event) -> None:
        task_id = event.row_key
        task = self.task_manager.get_task(int(task_id))
        if task:
            details = self.query_one("#task-details", Static)
            details.update(f"""
**Title:** {task.title}
**Description:** {task.description}
**Status:** {'Completed' if task.completed else 'Pending'}
**Created:** {task.created_at.strftime('%Y-%m-%d %H:%M')}
            """)
```

## Confirmation Dialogs

### Modal Confirmation
```python
from textual.screen import ModalScreen
from textual.containers import Container, Horizontal

class ConfirmDialog(ModalScreen[bool]):
    CSS = """
    ConfirmDialog {
        align: center middle;
    }

    #dialog {
        width: 50;
        height: auto;
        border: solid $error;
        background: $surface;
        padding: 2;
    }

    .title {
        text-align: center;
        text-style: bold;
        color: $error;
    }

    .message {
        text-align: center;
        padding: 1 0;
    }
    """

    def __init__(self, title: str, message: str):
        super().__init__()
        self.title_text = title
        self.message_text = message

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static(self.title_text, classes="title")
            yield Static(self.message_text, classes="message")
            yield Horizontal(
                Button("Confirm", variant="error", id="confirm"),
                Button("Cancel", variant="default", id="cancel")
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "confirm")

# Usage
def action_delete_task(self) -> None:
    table = self.query_one(DataTable)
    if table.cursor_row is None:
        return

    def handle_confirm(confirmed: bool) -> None:
        if confirmed:
            task_id = int(table.get_row_at(table.cursor_row)[0])
            self.task_manager.delete_task(task_id)
            self.refresh_table()

    self.push_screen(
        ConfirmDialog("Delete Task", "Are you sure?"),
        handle_confirm
    )
```

## Stats Dashboard

### Comprehensive Stats Widget
```python
from textual.widgets import Static
from rich.panel import Panel
from rich.table import Table

class StatsWidget(Static):
    def update_stats(self, stats: dict) -> None:
        table = Table.grid(padding=1)
        table.add_column(justify="right", style="bold")
        table.add_column(justify="left")

        table.add_row("Total:", f"[cyan]{stats['total']}[/]")
        table.add_row("Pending:", f"[yellow]{stats['pending']}[/]")
        table.add_row("Completed:", f"[green]{stats['completed']}[/]")
        table.add_row("Progress:", f"[blue]{stats['percentage']:.1f}%[/]")

        panel = Panel(table, title="📊 Statistics", border_style="blue")
        self.update(panel)

# Usage
stats_widget = self.query_one(StatsWidget)
stats_widget.update_stats(self.task_manager.get_stats())
```

### Real-time Counter
```python
from textual.reactive import reactive

class TodoApp(App):
    task_count = reactive(0)
    completed_count = reactive(0)

    def watch_task_count(self) -> None:
        self.update_stats_display()

    def watch_completed_count(self) -> None:
        self.update_stats_display()

    def update_stats_display(self) -> None:
        stats = self.query_one("#stats", Static)
        stats.update(
            f"Tasks: {self.task_count} | "
            f"Done: {self.completed_count} | "
            f"Remaining: {self.task_count - self.completed_count}"
        )
```

## Animations and Transitions

### Task Completion Animation
```python
from textual import work
from time import sleep

@work(thread=True)
async def animate_completion(self, task_id: int) -> None:
    """Animate task completion with visual feedback"""
    # Flash the row
    for _ in range(3):
        # Highlight
        self.add_class("flash-success")
        await sleep(0.1)
        # Remove highlight
        self.remove_class("flash-success")
        await sleep(0.1)

    # Update task
    self.task_manager.toggle_task(task_id)
    self.refresh_table()

CSS = """
.flash-success {
    background: $success 50%;
}
"""
```

### Smooth Loading
```python
from textual.widgets import LoadingIndicator

class TodoApp(App):
    def compose(self) -> ComposeResult:
        yield LoadingIndicator(id="loader")
        yield DataTable()

    async def on_mount(self) -> None:
        loader = self.query_one("#loader", LoadingIndicator)
        # Simulate loading
        await asyncio.sleep(1)
        loader.display = False
        self.refresh_table()
```

## Theme Support

### Dark/Light Toggle
```python
from textual.design import ColorSystem

class TodoApp(App):
    dark_mode = reactive(True)

    def watch_dark_mode(self, dark: bool) -> None:
        self.theme = "textual-dark" if dark else "textual-light"

    def action_toggle_theme(self) -> None:
        self.dark_mode = not self.dark_mode

    BINDINGS = [
        Binding("t", "toggle_theme", "Theme"),
    ]
```

### Custom Themes
```python
class TodoApp(App):
    CSS = """
    /* Light theme */
    Screen.light {
        background: #ffffff;
        color: #000000;
    }

    /* Dark theme */
    Screen.dark {
        background: #1e1e1e;
        color: #ffffff;
    }
    """

    def action_toggle_theme(self) -> None:
        screen = self.query_one(Screen)
        if screen.has_class("light"):
            screen.remove_class("light")
            screen.add_class("dark")
        else:
            screen.remove_class("dark")
            screen.add_class("light")
```

## Bulk Operations

### Multi-select with Checkboxes
```python
from textual.widgets import Checkbox

class TodoApp(App):
    selected_tasks = reactive(set())

    def compose(self) -> ComposeResult:
        yield Checkbox("Select All", id="select-all")
        yield DataTable()
        yield Horizontal(
            Button("Delete Selected", variant="error", id="bulk-delete"),
            Button("Complete Selected", variant="success", id="bulk-complete")
        )

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.checkbox.id == "select-all":
            if event.value:
                self.selected_tasks = {t.id for t in self.task_manager.tasks}
            else:
                self.selected_tasks = set()
            self.refresh_table()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "bulk-delete":
            for task_id in self.selected_tasks:
                self.task_manager.delete_task(task_id)
            self.selected_tasks = set()
            self.refresh_table()
```

### Quick Actions Footer
```python
class TodoApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Container(
            Button("Complete All ✓", id="complete-all"),
            Button("Clear Completed 🗑️", id="clear-completed"),
            Button("Delete All ⚠️", id="delete-all"),
            id="bulk-actions"
        )

    CSS = """
    #bulk-actions {
        height: 3;
        background: $panel;
        padding: 1;
    }
    """
```
