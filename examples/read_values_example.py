#!/usr/bin/env python3
"""
Example demonstrating how to read table values from UrwScrollTable.
"""

import urwid
from urw_scroll_table import UrwScrollTable


def main():
    """Demonstrate table value reading functionality."""
    # Sample data
    headers = ['Name', 'Age', 'City', 'Status']
    data = [
        ['Alice', 25, 'New York', 'Active'],
        ['Bob', 30, 'Los Angeles', 'Active'],
        ['Charlie', 35, 'Chicago', 'Inactive'],
        ['Diana', 28, 'Houston', 'Active'],
        ['Eve', 32, 'Phoenix', 'Pending']
    ]

    # Create table
    table = UrwScrollTable(
        headers=headers,
        data=data,
        max_height=10,
        column_types={
            0: 'editable', 1: 'editable', 2: 'editable', 3: 'dropdown'
        }
    )

    print("=== UrwScrollTable Value Reading Example ===\n")

    # Demonstrate different ways to read table data
    print("1. Get all table data:")
    all_data = table.get_all_data()
    for i, row in enumerate(all_data):
        print(f"   Row {i}: {row}")

    print("\n2. Get specific row data:")
    row_2 = table.get_row_data(2)
    print(f"   Row 2: {row_2}")

    print("\n3. Get specific cell value:")
    cell_value = table.get_cell_value(1, 2)
    print(f"   Cell (1,2): '{cell_value}'")

    print("\n4. Get table headers:")
    headers = table.get_headers()
    print(f"   Headers: {headers}")

    print("\n5. Get comprehensive table information:")
    info = table.get_table_info()
    print(f"   Dimensions: {info['dimensions']}")
    print(f"   Current position: {info['current_position']}")
    print(f"   Column types: {info['column_types']}")

    print("\n6. Simulate data modification and read again:")
    # Modify some data
    table.data[0][0] = 'Alice Modified'
    table.data[1][1] = 31

    # Read modified data
    modified_data = table.get_all_data()
    print(f"   Modified first row: {modified_data[0]}")
    print(f"   Modified second row: {modified_data[1]}")

    print("\n=== Example completed ===")


if __name__ == '__main__':
    main()
