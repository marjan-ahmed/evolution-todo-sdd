"""
Modern Terminal Todo App
Built with Textual framework for beautiful, interactive CLI experience
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Static,
)


# ============================================================================
# Data Models (Business Logic - Decoupled from UI)
# ============================================================================

@dataclass
class Task:
    """Represents a single todo task"""
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        status = "☑" if self.completed else "☐"
        return f"{status} {self.title}"


class TaskManager:
    """Manages todo tasks in memory - Business logic layer"""

    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task"""
        task = Task(
            id=self.next_id,
            title=title,
            description=description
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return next((t for t in self.tasks if t.id == task_id), None)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """Update task fields"""
        task = self.get_task(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def toggle_task(self, task_id: int) -> bool:
        """Toggle task completion status"""
        task = self.get_task(task_id)
        if task:
            task.completed = not task.completed
            return True
        return False

    def get_stats(self) -> dict:
        """Get task statistics"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        percentage = (completed / total * 100) if total > 0 else 0

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "percentage": percentage
        }


# ============================================================================
# UI Components (Screens and Modals)
# ============================================================================

class AddTaskScreen(ModalScreen[dict]):
    """Modal screen for adding a new task"""

    CSS = """
    AddTaskScreen {
        align: center middle;
    }

    #dialog {
        width: 60;
        height: auto;
        border: solid $primary;
        background: $surface;
        padding: 2;
    }

    .dialog-title {
        text-align: center;
        text-style: bold;
        color: $primary;
        padding-bottom: 1;
    }

    Input {
        margin: 1 0;
    }

    Horizontal {
        align: center middle;
        height: auto;
    }

    Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static("✨ Add New Task", classes="dialog-title")
            yield Input(placeholder="Task title (required)", id="title")
            yield Input(placeholder="Description (optional)", id="description")
            yield Horizontal(
                Button("Add", variant="success", id="add"),
                Button("Cancel", variant="default", id="cancel")
            )

    def on_mount(self) -> None:
        self.query_one("#title", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            title = self.query_one("#title", Input).value.strip()
            description = self.query_one("#description", Input).value.strip()

            if not title:
                # Could show error notification here
                return

            self.dismiss({"title": title, "description": description})
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)


class EditTaskScreen(ModalScreen[dict]):
    """Modal screen for editing an existing task"""

    CSS = """
    EditTaskScreen {
        align: center middle;
    }

    #dialog {
        width: 60;
        height: auto;
        border: solid $accent;
        background: $surface;
        padding: 2;
    }

    .dialog-title {
        text-align: center;
        text-style: bold;
        color: $accent;
        padding-bottom: 1;
    }

    Input {
        margin: 1 0;
    }

    Horizontal {
        align: center middle;
        height: auto;
    }

    Button {
        margin: 0 1;
    }
    """

    def __init__(self, task: Task):
        super().__init__()
        self.task = task

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static("✏️ Edit Task", classes="dialog-title")
            yield Input(
                value=self.task.title,
                placeholder="Task title",
                id="title"
            )
            yield Input(
                value=self.task.description,
                placeholder="Description",
                id="description"
            )
            yield Horizontal(
                Button("Save", variant="primary", id="save"),
                Button("Cancel", variant="default", id="cancel")
            )

    def on_mount(self) -> None:
        self.query_one("#title", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            title = self.query_one("#title", Input).value.strip()
            description = self.query_one("#description", Input).value.strip()

            if not title:
                return

            self.dismiss({"title": title, "description": description})
        else:
            self.dismiss(None)


class ConfirmDialog(ModalScreen[bool]):
    """Generic confirmation dialog"""

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

    .dialog-title {
        text-align: center;
        text-style: bold;
        color: $error;
        padding-bottom: 1;
    }

    .dialog-message {
        text-align: center;
        padding: 1 0;
    }

    Horizontal {
        align: center middle;
        height: auto;
    }

    Button {
        margin: 0 1;
    }
    """

    def __init__(self, title: str, message: str):
        super().__init__()
        self.title_text = title
        self.message_text = message

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static(self.title_text, classes="dialog-title")
            yield Static(self.message_text, classes="dialog-message")
            yield Horizontal(
                Button("Confirm", variant="error", id="confirm"),
                Button("Cancel", variant="default", id="cancel")
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "confirm")


# ============================================================================
# Main Application
# ============================================================================

class TodoApp(App):
    """Modern Terminal Todo Application"""

    CSS = """
    Screen {
        background: $surface;
    }

    #stats {
        height: 3;
        background: $panel;
        border: solid $secondary;
        padding: 1;
        text-align: center;
        color: $text;
    }

    DataTable {
        height: 1fr;
        border: solid $primary;
        margin: 1 0;
    }

    .completed {
        text-style: strike;
        color: $success;
    }

    .pending {
        color: $text;
    }
    """

    BINDINGS = [
        Binding("a", "add_task", "Add Task", show=True),
        Binding("e", "edit_task", "Edit", show=True),
        Binding("d", "delete_task", "Delete", show=True),
        Binding("space", "toggle_task", "Toggle", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(id="stats")
        yield DataTable(zebra_stripes=True, cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app"""
        table = self.query_one(DataTable)
        table.add_columns("ID", "Status", "Title", "Description")
        table.focus()

        # Add some demo tasks
        self.task_manager.add_task("Welcome to Todo App", "Press 'a' to add new task")
        self.task_manager.add_task("Try keyboard shortcuts", "Press 'space' to toggle, 'd' to delete")
        self.task_manager.add_task("Check out the stats", "See the stats panel at the top")

        self.refresh_ui()

    def refresh_ui(self) -> None:
        """Refresh the entire UI"""
        self.refresh_table()
        self.refresh_stats()

    def refresh_table(self) -> None:
        """Update the task table"""
        table = self.query_one(DataTable)
        table.clear()

        for task in self.task_manager.tasks:
            status = "☑" if task.completed else "☐"
            style = "completed" if task.completed else "pending"

            table.add_row(
                str(task.id),
                status,
                task.title,
                task.description,
                key=str(task.id)
            )

    def refresh_stats(self) -> None:
        """Update the statistics display"""
        stats = self.task_manager.get_stats()
        stats_widget = self.query_one("#stats", Static)

        stats_widget.update(
            f"📊 Total: {stats['total']} | "
            f"⏳ Pending: {stats['pending']} | "
            f"✅ Completed: {stats['completed']} | "
            f"📈 Progress: {stats['percentage']:.1f}%"
        )

    def action_add_task(self) -> None:
        """Add a new task"""
        def handle_result(result: dict | None) -> None:
            if result:
                self.task_manager.add_task(
                    result["title"],
                    result["description"]
                )
                self.refresh_ui()

        self.push_screen(AddTaskScreen(), handle_result)

    def action_edit_task(self) -> None:
        """Edit the selected task"""
        table = self.query_one(DataTable)
        if table.cursor_row is None:
            return

        row_key = table.get_row_at(table.cursor_row)[0]
        task = self.task_manager.get_task(int(row_key))

        if not task:
            return

        def handle_result(result: dict | None) -> None:
            if result:
                self.task_manager.update_task(
                    task.id,
                    result["title"],
                    result["description"]
                )
                self.refresh_ui()

        self.push_screen(EditTaskScreen(task), handle_result)

    def action_delete_task(self) -> None:
        """Delete the selected task with confirmation"""
        table = self.query_one(DataTable)
        if table.cursor_row is None:
            return

        row_key = table.get_row_at(table.cursor_row)[0]
        task = self.task_manager.get_task(int(row_key))

        if not task:
            return

        def handle_confirm(confirmed: bool) -> None:
            if confirmed:
                self.task_manager.delete_task(task.id)
                self.refresh_ui()

        self.push_screen(
            ConfirmDialog(
                "🗑️ Delete Task",
                f"Delete '{task.title}'?"
            ),
            handle_confirm
        )

    def action_toggle_task(self) -> None:
        """Toggle completion status of selected task"""
        table = self.query_one(DataTable)
        if table.cursor_row is None:
            return

        row_key = table.get_row_at(table.cursor_row)[0]
        task_id = int(row_key)

        self.task_manager.toggle_task(task_id)
        self.refresh_ui()


def main():
    """Entry point"""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
