#!/usr/bin/env python3
"""
Demo script for urw-scroll-table package.

This script demonstrates how to use the UrwScrollTable widget
in a urwid application.
"""

import urwid
from urw_scroll_table import UrwScrollTable


class DemoApp:
    """Demo application for the UrwScrollTable widget."""

    def __init__(self, edit_color='yellow', colors=None):
        self.edit_color = edit_color
        self.colors = colors or {}

        # Sample data
        self.headers = ['Name', 'Age', 'City', 'Status', 'Notes']
        self.data = [
            ['Alice', 25, 'New York', 'Active', 'Developer'],
            ['Bob', 30, 'Los Angeles', 'Active', 'Manager'],
            ['Charlie', 35, 'Chicago', 'Active', 'Designer'],
            ['Diana', 28, 'Houston', 'Active', 'Engineer'],
            ['Eve', 32, 'Phoenix', 'Inactive', 'Analyst'],
            ['Frank', 27, 'Philadelphia', 'Active', 'Developer'],
            ['Grace', 29, 'San Antonio', 'Active', 'Manager'],
            ['Henry', 31, 'San Diego', 'Active', 'Designer'],
            ['Ivy', 26, 'Dallas', 'Active', 'Engineer'],
            ['Jack', 33, 'San Jose', 'Active', 'Analyst'],
            ['2nd Diana', 28, 'Houston', 'Active', 'Engineer'],
            ['2nd Eve', 32, 'Phoenix', 'Inactive', 'Analyst'],
            ['2nd Frank', 27, 'Philadelphia', 'Active', 'Developer'],
            ['2nd Grace', 29, 'San Antonio', 'Active', 'Manager'],
            ['2nd Henry', 31, 'San Diego', 'Active', 'Designer'],
            ['3rd Ivy', 26, 'Dallas', 'Active', 'Engineer'],
            ['3rd Jack', 33, 'San Jose', 'Active', 'Analyst'],
            ['4th Alice', 25, 'New York', 'Active', 'Developer'],
            ['4th Bob', 30, 'Los Angeles', 'Active', 'Manager'],
            ['4th Charlie', 35, 'Chicago', 'Active', 'Designer'],
            ['4th Diana', 28, 'Houston', 'Active', 'Engineer'],
            ['4th Eve', 32, 'Phoenix', 'Inactive', 'Analyst'],
            ['4th Frank', 27, 'Philadelphia', 'Active', 'Developer'],
            ['4th Grace', 29, 'San Antonio', 'Active', 'Manager'],
            ['4th Henry', 31, 'San Diego', 'Active', 'Designer'],
            ['4th Ivy', 26, 'Dallas', 'Active', 'Engineer'],
            ['4th Jack', 33, 'San Jose', 'Active', 'Analyst'],
            ['5th Charlie', 35, 'Chicago', 'Active', 'Designer'],
            ['5th Diana', 28, 'Houston', 'Active', 'Engineer'],
            ['5th Eve', 32, 'Phoenix', 'Inactive', 'Analyst'],
            ['5th Frank', 27, 'Philadelphia', 'Active', 'Developer'],
            ['5th Grace', 29, 'San Antonio', 'Active', 'Manager'],
            ['5th Henry', 31, 'San Diego', 'Active', 'Designer'],
            ['5th Ivy', 26, 'Dallas', 'Active', 'Engineer'],
            ['5th Jack', 33, 'San Jose', 'Active', 'Analyst'],
        ]

        # Define column types
        self.column_types = {
            0: 'editable',    # Name - editable text
            1: 'editable',    # Age - editable text
            2: 'editable',    # City - editable text
            3: 'dropdown',    # Status - dropdown
            4: 'editable',    # Notes - editable text
        }

        # Create the table widget
        self.table = UrwScrollTable(
            headers=self.headers,
            data=self.data,
            edit_color=self.edit_color,
            column_types=self.column_types,
            colors=self.colors
        )

        # Create the main UI
        self._setup_ui()

    def _setup_ui(self):
        """Set up the main UI components."""
        # Create a frame with the table as the body
        self.frame = urwid.Frame(
            body=self.table,
            header=urwid.Text(
                'UrwScrollTable Demo - Use arrow keys to navigate, '
                'Enter to edit, q to quit',
                align='center'
            ),
            footer=urwid.Text('Status: Ready', align='center')
        )

        # Set up the color palette
        self._setup_palette()

    def _setup_palette(self):
        """Set up the color palette."""
        self.palette = [
            ('header', *self.colors.get('header', ('white', 'dark blue'))),
            ('selected', *self.colors.get('active_cell', ('black', 'white'))),
            ('edit', *self.colors.get(
                'editing_cell', ('black', self.edit_color)
            )),
            ('status', *self.colors.get('status', ('white', 'black'))),
        ]

    def run(self):
        """Run the application."""
        # Create the main loop
        loop = urwid.MainLoop(
            self.frame,
            palette=self.palette,
            unhandled_input=self._handle_input,
            screen=urwid.display.raw.Screen()
        )
        # Run the loop
        loop.run()

    def _handle_input(self, key):
        """Handle unhandled input."""
        if key == 'q':
            raise urwid.ExitMainLoop()


def main():
    """Main entry point."""
    import sys

    # Parse command line arguments for edit color
    edit_color = 'yellow'  # default
    if len(sys.argv) > 1:
        edit_color = sys.argv[1]

    # Validate color
    foreground_colors = [
        'black', 'dark red', 'dark green', 'brown', 'dark blue',
        'dark magenta', 'dark cyan', 'light gray', 'dark gray',
        'light red', 'light green', 'yellow', 'light blue',
        'light magenta', 'light cyan', 'white']

    if edit_color not in foreground_colors:
        print(
            f"Warning: '{edit_color}' is not a valid urwid color. "
            f"Using 'yellow' instead."
        )
        edit_color = 'yellow'

    # Example of custom colors (you can modify these)
    custom_colors = {
        'header': ('dark blue', 'light red', 'default', '#00f', '#ff0'),
        'active_cell': ('white', 'light green', 'default', '#999', '#12f'),
        'editing_cell': ('dark blue', 'dark green', 'default', '#005', '#0f0'),
        'status': ('white', 'black', 'default', '#999', '#000')
    }

    # Create and run the application
    app = DemoApp(edit_color=edit_color, colors=custom_colors)
    app.run()


if __name__ == '__main__':
    main()
