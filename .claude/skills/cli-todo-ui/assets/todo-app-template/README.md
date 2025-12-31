# Modern Terminal Todo App

A beautiful, interactive terminal-based todo application built with Textual.

## Features

- ✨ Modern TUI with menu-driven flows
- 🎨 Color-coded status indicators
- ⌨️ Keyboard shortcuts for all actions
- 🖱️ Mouse support
- 📊 Real-time statistics
- ✅ Task completion tracking
- 🗑️ Confirmation dialogs for destructive actions

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

## Keyboard Shortcuts

- `a` - Add new task
- `e` - Edit selected task
- `d` - Delete selected task
- `space` - Toggle task completion
- `↑/↓` - Navigate tasks
- `q` - Quit

## Architecture

The app follows a clean separation between business logic (`TaskManager`) and UI (`TodoApp`), making it easy to:

- Add persistence (save to file/database)
- Extend with new features
- Test independently
- Reuse business logic in different interfaces

## Customization

Edit the `CSS` strings in `app.py` to customize colors, spacing, and layout. See [Textual documentation](https://textual.textualize.io/) for styling options.
