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


if __name__ == '__main__':
    pytest.main([__file__])