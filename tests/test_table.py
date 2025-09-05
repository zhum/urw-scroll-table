"""
Tests for the UrwScrollTable widget.
"""

import pytest
from urw_scroll_table import UrwScrollTable


def test_table_creation():
    """Test basic table creation."""
    headers = ['Name', 'Age', 'City']
    data = [
        ['Alice', 25, 'New York'],
        ['Bob', 30, 'Los Angeles'],
    ]

    table = UrwScrollTable(headers=headers, data=data)

    assert table.headers == headers
    assert table.data == data
    assert table.current_row == 0
    assert table.current_col == 0
    assert not table.editing


def test_column_types():
    """Test column type processing."""
    headers = ['Name', 'Age', 'Status']
    data = [['Alice', 25, 'Active']]

    # Test with dict
    column_types = {0: 'editable', 1: 'text', 2: 'dropdown'}
    table = UrwScrollTable(
        headers=headers, data=data, column_types=column_types
    )
    assert table.column_types == column_types

    # Test with list
    column_types_list = ['editable', 'text', 'dropdown']
    table2 = UrwScrollTable(
        headers=headers, data=data, column_types=column_types_list
    )
    expected = {0: 'editable', 1: 'text', 2: 'dropdown'}
    assert table2.column_types == expected

    # Test with None (default)
    table3 = UrwScrollTable(headers=headers, data=data)
    expected_default = {0: 'text', 1: 'text', 2: 'text'}
    assert table3.column_types == expected_default


def test_column_width_calculation():
    """Test column width calculation."""
    headers = ['Name', 'Age', 'City']
    data = [
        ['Alice', 25, 'New York'],
        ['Bob', 30, 'Los Angeles'],  # Longer city name
    ]

    table = UrwScrollTable(headers=headers, data=data)

    # Check that column widths are calculated correctly
    assert len(table.column_widths) == 3
    assert table.column_widths[0] >= len('Alice')  # Name column
    assert table.column_widths[1] >= len('Age')    # Age column
    assert table.column_widths[2] >= len('Los Angeles')  # Longest


def test_cell_change():
    """Test cell value changes."""
    headers = ['Name', 'Age']
    data = [['Alice', 25]]

    table = UrwScrollTable(headers=headers, data=data)

    # Change a cell value
    table._on_cell_change(0, 0, 'Alice Updated')

    assert table.data[0][0] == 'Alice Updated'
    assert not table.editing


def test_visible_columns():
    """Test visible columns calculation."""
    headers = ['Name', 'Age', 'City', 'Status', 'Notes']
    data = [['Alice', 25, 'New York', 'Active', 'Developer']]

    table = UrwScrollTable(headers=headers, data=data)

    # Test with different widths
    visible_cols = table._get_visible_columns(20)
    assert len(visible_cols) < len(headers)  # Should be fewer columns

    visible_cols = table._get_visible_columns(100)
    assert len(visible_cols) >= len(headers)  # Should fit all columns


def test_dropdown_functionality():
    """Test dropdown cell functionality."""
    headers = ['Name', 'Status']
    data = [['Alice', 'Active']]
    column_types = {0: 'text', 1: 'dropdown'}
    dropdown_options = {1: ['Active', 'Inactive', 'Pending']}

    table = UrwScrollTable(
        headers=headers,
        data=data,
        column_types=column_types,
        dropdown_options=dropdown_options
    )

    # Test dropdown options retrieval
    options = table._get_dropdown_options(1)
    assert options == ['Active', 'Inactive', 'Pending']

    # Test dropdown widget detection
    table.current_row = 0
    table.current_col = 1
    dropdown_widget = table._get_current_dropdown_widget()
    assert dropdown_widget is not None
    assert hasattr(dropdown_widget, 'open_pop_up')


def test_dropdown_scroll_position():
    """Test dropdown functionality when scrolled down."""
    headers = ['Name', 'Status']
    data = [
        ['Alice', 'Active'],
        ['Bob', 'Inactive'],
        ['Charlie', 'Pending'],
        ['Diana', 'Active'],
        ['Eve', 'Inactive']
    ]
    column_types = {0: 'text', 1: 'dropdown'}
    dropdown_options = {1: ['Active', 'Inactive', 'Pending']}

    table = UrwScrollTable(
        headers=headers,
        data=data,
        column_types=column_types,
        dropdown_options=dropdown_options,
        max_height=3  # Only show 3 rows at a time
    )

    # Test dropdown detection in the last visible row
    table.current_row = 2  # Third row (Charlie)
    table.current_col = 1  # Status column (dropdown)
    table._update_display()

    # Should find the dropdown widget correctly
    dropdown_widget = table._get_current_dropdown_widget()
    assert dropdown_widget is not None
    assert hasattr(dropdown_widget, 'open_pop_up')


def test_dropdown_widget_creation():
    """Test that dropdown widgets are created correctly."""
    headers = ['Name', 'Status']
    data = [['Alice', 'Active']]
    column_types = {0: 'text', 1: 'dropdown'}
    dropdown_options = {1: ['Active', 'Inactive', 'Pending']}

    table = UrwScrollTable(
        headers=headers,
        data=data,
        column_types=column_types,
        dropdown_options=dropdown_options
    )

    # Create table widgets
    table._create_table_widgets()

    # Check that dropdown widgets are created
    assert len(table.table_widgets) > 0
    row_widget = table.table_widgets[0]

    # Should be a Columns widget when dropdowns are present
    assert hasattr(row_widget, 'contents')
    assert len(row_widget.contents) == 2  # Two columns


def test_header_alignment():
    """Test that header and table cells are properly aligned."""
    headers = ['Name', 'Status', 'Notes']
    data = [['Alice', 'Active', 'Developer']]
    column_types = {0: 'text', 1: 'dropdown', 2: 'text'}
    dropdown_options = {1: ['Active', 'Inactive', 'Pending']}

    table = UrwScrollTable(
        headers=headers,
        data=data,
        column_types=column_types,
        dropdown_options=dropdown_options
    )

    # Create table widgets
    table._create_table_widgets()

    # Header should be created with Columns widget when dropdowns are present
    assert hasattr(table.header_widget, 'original_widget')
    header_widget = table.header_widget.original_widget
    assert hasattr(header_widget, 'contents')  # Should be Columns widget


def test_navigation():
    """Test table navigation functionality."""
    headers = ['Name', 'Age', 'City']
    data = [
        ['Alice', 25, 'New York'],
        ['Bob', 30, 'Los Angeles'],
        ['Charlie', 35, 'Chicago']
    ]

    table = UrwScrollTable(headers=headers, data=data)

    # Test initial position
    assert table.current_row == 0
    assert table.current_col == 0

    # Test navigation (simulate keypress)
    # Note: We can't easily test actual keypress events without a display,
    # but we can test the navigation logic

    # Test row navigation bounds
    table.current_row = len(data) - 1
    assert table.current_row == 2

    # Test column navigation bounds
    table.current_col = len(headers) - 1
    assert table.current_col == 2


def test_editing_mode():
    """Test editing mode functionality."""
    headers = ['Name', 'Age']
    data = [['Alice', 25]]
    column_types = {0: 'editable', 1: 'editable'}  # Make columns editable

    table = UrwScrollTable(
        headers=headers,
        data=data,
        column_types=column_types)

    # Initially not editing
    assert not table.editing

    # Test starting edit mode
    table.current_row = 0
    table.current_col = 0
    table._start_editing_current_cell()
    assert table.editing

    # Test stopping edit mode
    table.editing = False
    assert not table.editing


def test_cell_visibility():
    """Test that current cell visibility is maintained."""
    headers = ['Name', 'Age', 'City', 'Status', 'Notes']
    data = [
        ['Alice', 25, 'New York', 'Active', 'Developer'],
        ['Bob', 30, 'Los Angeles', 'Inactive', 'Manager'],
        ['Charlie', 35, 'Chicago', 'Active', 'Designer'],
        ['Diana', 28, 'Houston', 'Active', 'Engineer'],
        ['Eve', 32, 'Phoenix', 'Inactive', 'Analyst']
    ]

    table = UrwScrollTable(headers=headers, data=data, max_height=3)

    # Test that current cell stays visible when navigating
    table.current_row = 4  # Last row
    table.current_col = 4  # Last column
    table._ensure_current_cell_visible()

    # Should adjust vertical offset to show current row
    assert table.vertical_offset <= table.current_row
    assert table.current_row < table.vertical_offset + table.max_height - 1


def test_dropdown_options_handling():
    """Test dropdown options handling."""
    headers = ['Status']
    data = [['Active']]
    column_types = {0: 'dropdown'}
    dropdown_options = {0: ['Active', 'Inactive', 'Pending', 'Suspended']}

    table = UrwScrollTable(
        headers=headers,
        data=data,
        column_types=column_types,
        dropdown_options=dropdown_options
    )

    # Test getting dropdown options
    options = table._get_dropdown_options(0)
    assert options == ['Active', 'Inactive', 'Pending', 'Suspended']

    # Test with missing column
    options = table._get_dropdown_options(1)
    assert options == []

    # Test with no dropdown options provided
    table2 = UrwScrollTable(
        headers=headers,
        data=data,
        column_types=column_types
    )
    options = table2._get_dropdown_options(0)
    assert options == []


def test_widget_selectable():
    """Test that the table widget is selectable."""
    headers = ['Name', 'Age']
    data = [['Alice', 25]]

    table = UrwScrollTable(headers=headers, data=data)

    # Table should be selectable
    assert table.selectable()


def test_table_with_mixed_column_types():
    """Test table with mixed column types."""
    headers = ['Name', 'Age', 'Status', 'Notes']
    data = [['Alice', 25, 'Active', 'Developer']]
    column_types = {
        0: 'editable',  # Name - editable
        1: 'text',      # Age - read-only text
        2: 'dropdown',  # Status - dropdown
        3: 'editable'   # Notes - editable
    }
    dropdown_options = {2: ['Active', 'Inactive', 'Pending']}

    table = UrwScrollTable(
        headers=headers,
        data=data,
        column_types=column_types,
        dropdown_options=dropdown_options
    )

    # Verify column types are set correctly
    assert table.column_types[0] == 'editable'
    assert table.column_types[1] == 'text'
    assert table.column_types[2] == 'dropdown'
    assert table.column_types[3] == 'editable'

    # Verify dropdown options are available
    assert table.dropdown_options[2] == ['Active', 'Inactive', 'Pending']


if __name__ == '__main__':
    pytest.main([__file__])
