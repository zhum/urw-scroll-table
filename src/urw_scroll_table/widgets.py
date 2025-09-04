"""
Widget classes for the urw-scroll-table package.

This module contains all the supporting widget classes used by the main table.
"""

import urwid


class SafeText(urwid.Text):
    """A text widget that safely handles size parameters."""

    def render(self, size, focus=False):
        """Override render to handle size parameter correctly."""
        if isinstance(size, tuple) and len(size) > 1:
            # If we get a tuple with multiple values, use only the first one
            size = (size[0],)
        return super().render(size, focus)

    def rows(self, size, focus=False):
        """Override rows to handle size parameter correctly."""
        if isinstance(size, tuple) and len(size) > 1:
            # Use only the width for calculating rows
            size = (size[0],)
        return super().rows(size, focus)

    def pack(self, size=None, focus=False):
        """Override pack to handle size parameter correctly."""
        if isinstance(size, tuple) and len(size) > 1:
            # If we get a tuple with multiple values, use only the first one
            size = (size[0],)
        return super().pack(size, focus)


class SingleLineText(urwid.Text):
    """A text widget that always renders as a single line."""

    def __init__(self, text):
        # Replace newlines with spaces to ensure single line
        if isinstance(text, str):
            text = text.replace('\n', ' ')
        super().__init__(text)

    def rows(self, size, focus=False):
        """Always return 1 row."""
        return 1

    def render(self, size, focus=False):
        """Render the widget, ensuring only width is considered."""
        # Extract width from size tuple
        if isinstance(size, tuple) and len(size) > 1:
            size = (size[0],)
        return super().render(size, focus)


class HeightEnforcer(urwid.WidgetWrap):
    """
    A wrapper that forces any widget to always return
    exactly 1 row height.
    """

    def __init__(self, widget):
        super().__init__(widget)

    def rows(self, size, focus=False):
        """Always return 1 row, regardless of the wrapped widget."""
        return 1


class EditableCell(urwid.Edit):
    """A cell widget that can be edited."""

    def __init__(self, content="", on_change=None):
        # Convert content to string if it's not already
        if not isinstance(content, str):
            content = str(content)

        super().__init__("", content)
        self._original_content = content
        self.on_change = on_change

    def get_edit_text(self):
        """Get the current edit text."""
        return super().get_edit_text()

    def set_edit_text(self, text):
        """Set the edit text."""
        # Convert text to string if it's not already
        if not isinstance(text, str):
            text = str(text)
        super().set_edit_text(text)

    def keypress(self, size, key):
        """Handle keypress events."""
        # Let the parent Edit widget handle all keypresses
        # Enter and Esc are handled at the table level
        result = super().keypress(size, key)
        if result is None:
            # Key was handled, update original content
            self._original_content = self.get_edit_text()
        return result

    def render(self, size, focus=False):
        """Render the widget."""
        # Ensure size is a single value for width
        if isinstance(size, tuple) and len(size) > 1:
            size = (size[0],)
        return super().render(size, focus)

    def rows(self, size, focus=False):
        """Return the number of rows."""
        # Always return 1 row
        return 1

    def pack(self, size, focus=False):
        """Pack the widget."""
        # Ensure size is a single value for width
        if isinstance(size, tuple) and len(size) > 1:
            size = (size[0],)
        return super().pack(size, focus)


class DropdownCell(urwid.WidgetWrap):
    """A dropdown cell widget with compact inline display."""

    def __init__(self, content="", options=None, on_change=None):
        """
        Initialize dropdown cell.

        Args:
            content: Current selected value
            options: List of available options
            on_change: Callback function when selection changes
        """
        self.options = options or []
        self.on_change = on_change
        self._original_content = content
        self.current_index = self._get_index_for_content(content)
        self.expanded = False

        # Create the main text widget
        self.text_widget = SingleLineText(content)
        self._update_display()

        # Start with the text widget
        super().__init__(self.text_widget)

    def _get_index_for_content(self, content):
        """Get the index for the given content."""
        try:
            return self.options.index(content)
        except ValueError:
            return 0 if self.options else -1

    def _update_display(self):
        """Update the display text."""
        if self.expanded:
            # Show compact dropdown display
            self._show_compact_dropdown()
        else:
            # Show single line with current selection
            if self.options and 0 <= self.current_index < len(self.options):
                display_text = self.options[self.current_index]
            else:
                display_text = self._original_content

            display_text += " ▶"
            self.text_widget.set_text(display_text)
            self._w = self.text_widget

    def _show_compact_dropdown(self):
        """Show a compact dropdown display that fits in the cell."""
        if not self.options:
            self.text_widget.set_text("No options ▶")
            self._w = self.text_widget
            return

        # Show current selection and navigation hint
        if 0 <= self.current_index < len(self.options):
            current_text = f"▶ {self.options[self.current_index]}"
        else:
            current_text = "▶ No selection"

        # Add navigation hint
        hint = f" (↑↓ {self.current_index + 1}/{len(self.options)})"

        # Truncate if too long
        max_len = 35  # Adjust based on typical cell width
        if len(current_text) + len(hint) > max_len:
            current_text = current_text[:max_len - len(hint)] + "..."

        display_text = current_text + hint
        self.text_widget.set_text(display_text)
        self._w = self.text_widget

    def keypress(self, size, key):
        """Handle keypress events."""
        if not self.options:
            return key

        if key == 'enter':
            if self.expanded:
                # Select current option and close dropdown
                if 0 <= self.current_index < len(self.options):
                    selected_value = self.options[self.current_index]
                    self._original_content = selected_value
                    # Don't call on_change here - handled by table
                self.expanded = False
                self._update_display()
                return None
            else:
                # Open dropdown
                self.expanded = True
                self._update_display()
                return None
        elif key == 'esc':
            # Cancel editing - restore original content
            self.expanded = False
            self.current_index = self._get_index_for_content(
                self._original_content
            )
            self._update_display()
            # Don't call on_change here - handled by table
            return None
        elif key == 'up' and self.expanded:
            # Move up in dropdown
            if self.current_index > 0:
                self.current_index -= 1
                self._update_display()
            return None
        elif key == 'down' and self.expanded:
            # Move down in dropdown
            if self.current_index < len(self.options) - 1:
                self.current_index += 1
                self._update_display()
            return None
        else:
            return key

    def render(self, size, focus=False):
        """Override render to handle size parameter correctly."""
        if isinstance(size, tuple) and len(size) > 1:
            # If we get a tuple with multiple values, use only the first one
            size = (size[0],)
        return super().render(size, focus)

    def rows(self, size, focus=False):
        """Override rows to handle size parameter correctly."""
        if isinstance(size, tuple) and len(size) > 1:
            # Use only the width for calculating rows
            size = (size[0],)

        # Always return 1 row - compact display
        return 1

    def get_edit_text(self):
        """Get the current selected value."""
        if self.expanded and 0 <= self.current_index < len(self.options):
            return self.options[self.current_index]
        else:
            return self._original_content
