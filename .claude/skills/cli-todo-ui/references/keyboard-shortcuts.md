# Keyboard Shortcuts Reference

Standard keyboard binding patterns for todo applications.

## Standard Todo App Shortcuts

### Navigation
- `↑/↓` or `j/k` - Navigate up/down in list
- `Home/End` - Jump to first/last task
- `PgUp/PgDown` - Scroll by page
- `Tab` - Move between sections
- `Escape` - Close modal/cancel operation

### Actions
- `a` - Add new task
- `e` - Edit selected task
- `d` - Delete selected task
- `space` - Toggle task completion
- `Enter` - Open task details
- `x` - Mark as complete
- `r` - Mark as pending (reopen)

### Filtering & Search
- `/` - Focus search input
- `f` - Show filter menu
- `1` - Show all tasks
- `2` - Show active tasks
- `3` - Show completed tasks

### Bulk Operations
- `Ctrl+a` - Select all
- `Ctrl+d` - Deselect all
- `Shift+↑/↓` - Multi-select

### Application
- `?` - Show help/shortcuts
- `t` - Toggle theme
- `Ctrl+s` - Save (if persistence)
- `Ctrl+e` - Export
- `q` - Quit application

## Implementation in Textual

### Basic Bindings
```python
from textual.binding import Binding

class TodoApp(App):
    BINDINGS = [
        # Task management
        Binding("a", "add_task", "Add Task", show=True),
        Binding("e", "edit_task", "Edit", show=True),
        Binding("d", "delete_task", "Delete", show=True),
        Binding("space", "toggle_task", "Toggle", show=True),

        # Navigation
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),

        # View management
        Binding("1", "show_all", "All", show=True),
        Binding("2", "show_active", "Active", show=True),
        Binding("3", "show_completed", "Completed", show=True),

        # Search and filter
        Binding("slash", "focus_search", "Search", key_display="/"),
        Binding("f", "toggle_filter", "Filter"),

        # Application
        Binding("question_mark", "show_help", "Help", key_display="?"),
        Binding("t", "toggle_theme", "Theme"),
        Binding("q", "quit", "Quit", show=True),
    ]

    def action_add_task(self) -> None:
        self.push_screen(AddTaskScreen())

    def action_edit_task(self) -> None:
        # Edit selected task
        pass

    def action_delete_task(self) -> None:
        # Delete with confirmation
        pass

    def action_toggle_task(self) -> None:
        # Toggle completion status
        pass

    def action_show_all(self) -> None:
        self.filter_mode = "all"
        self.refresh_table()

    def action_show_active(self) -> None:
        self.filter_mode = "active"
        self.refresh_table()

    def action_show_completed(self) -> None:
        self.filter_mode = "completed"
        self.refresh_table()

    def action_focus_search(self) -> None:
        self.query_one("#search", Input).focus()

    def action_show_help(self) -> None:
        self.push_screen(HelpScreen())

    def action_toggle_theme(self) -> None:
        self.dark = not self.dark
```

### Vim-style Navigation
```python
class TodoApp(App):
    BINDINGS = [
        # Vim movement
        Binding("j", "cursor_down", "Down"),
        Binding("k", "cursor_up", "Up"),
        Binding("g,g", "cursor_top", "Top"),  # gg
        Binding("shift+g", "cursor_bottom", "Bottom"),  # G

        # Vim actions
        Binding("d,d", "delete_task", "Delete"),  # dd
        Binding("y,y", "copy_task", "Copy"),  # yy
        Binding("p", "paste_task", "Paste"),  # p
    ]

    def action_cursor_down(self) -> None:
        table = self.query_one(DataTable)
        table.action_cursor_down()

    def action_cursor_up(self) -> None:
        table = self.query_one(DataTable)
        table.action_cursor_up()

    def action_cursor_top(self) -> None:
        table = self.query_one(DataTable)
        table.move_cursor(row=0)

    def action_cursor_bottom(self) -> None:
        table = self.query_one(DataTable)
        table.move_cursor(row=table.row_count - 1)
```

### Context-Sensitive Bindings
```python
class AddTaskScreen(ModalScreen):
    """Modal with its own bindings"""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("ctrl+s", "save", "Save"),
        Binding("enter", "save", "Save", show=False),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)

    def action_save(self) -> None:
        title = self.query_one("#title", Input).value
        if title:
            self.dismiss({"title": title})
```

### Dynamic Bindings
```python
class TodoApp(App):
    def watch_selected_count(self, count: int) -> None:
        """Update bindings based on selection"""
        if count > 0:
            self.bind("ctrl+d", "delete_selected", "Delete Selected")
            self.bind("ctrl+x", "complete_selected", "Complete Selected")
        else:
            self.unbind("ctrl+d")
            self.unbind("ctrl+x")
```

## Help Screen Implementation

```python
from textual.screen import Screen
from textual.widgets import Static
from rich.table import Table

class HelpScreen(Screen):
    """Display keyboard shortcuts"""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("q", "dismiss", "Close"),
    ]

    def compose(self) -> ComposeResult:
        shortcuts = Table(title="Keyboard Shortcuts", show_header=True)
        shortcuts.add_column("Key", style="cyan")
        shortcuts.add_column("Action", style="white")

        shortcuts.add_row("a", "Add new task")
        shortcuts.add_row("e", "Edit selected task")
        shortcuts.add_row("d", "Delete selected task")
        shortcuts.add_row("space", "Toggle task completion")
        shortcuts.add_row("Enter", "View task details")
        shortcuts.add_row("↑/↓", "Navigate tasks")
        shortcuts.add_row("/", "Search tasks")
        shortcuts.add_row("1/2/3", "Filter: All/Active/Completed")
        shortcuts.add_row("t", "Toggle theme")
        shortcuts.add_row("?", "Show this help")
        shortcuts.add_row("q", "Quit application")

        yield Static(shortcuts)

    def action_dismiss(self) -> None:
        self.app.pop_screen()
```

## Global vs Local Bindings

### App-level (Global)
```python
class TodoApp(App):
    """Bindings available everywhere"""
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("?", "show_help", "Help"),
    ]
```

### Widget-level (Local)
```python
class TaskTable(DataTable):
    """Bindings only when this widget is focused"""
    BINDINGS = [
        Binding("enter", "view_details", "Details"),
        Binding("space", "toggle", "Toggle"),
    ]

    def action_view_details(self) -> None:
        # Show task details
        pass

    def action_toggle(self) -> None:
        # Toggle selected task
        pass
```

## Accessibility Considerations

- Always provide `show=True` for primary actions in BINDINGS
- Include `key_display` for special keys (e.g., `/`, `?`)
- Support both arrow keys and vim-style (j/k) navigation
- Provide visual feedback in footer for available shortcuts
- Include help screen accessible via `?`
- Support both Enter and Ctrl+S for form submission
- Allow Escape to cancel operations consistently

## Best Practices

1. **Consistency**: Use standard conventions (e.g., `q` for quit, `?` for help)
2. **Visibility**: Show important shortcuts in footer
3. **Discoverability**: Include help screen with all shortcuts
4. **Context**: Disable inapplicable shortcuts based on state
5. **Feedback**: Visual confirmation when shortcut is triggered
6. **Documentation**: Keep help screen updated with all bindings
