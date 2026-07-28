# Stock Balance Report

## Overview

The Stock Balance report displays the current inventory balance for each item in each warehouse as of a selected date. It summarizes stock quantities and values by aggregating Stock Ledger Entries, providing an overview of inventory levels and valuation.

## Purpose

The report helps users:

- View available stock quantities for each item.
- Monitor inventory across warehouses.
- Determine the total inventory value.
- Analyze stock balances as of a specific date.
- Filter results by item or warehouse.

## Report Filters

| Filter | Description |
| -------- | ----------- |
| **As On Date** | Displays stock balances up to and including the selected date. Defaults to today's date. |
| **Item** | Limits the report to a specific inventory item. |
| **Warehouse** | Limits the report to a specific warehouse. |

## Report Columns

| Column | Description |
| -------- | ----------- |
| **Item** | The inventory item. |
| **Warehouse** | The warehouse where the stock is stored. |
| **Balance Qty** | The current quantity available in the warehouse. |
| **Valuation Rate** | The calculated average valuation rate (`Balance Value ÷ Balance Qty`). |
| **Balance Value** | The total inventory value for the item in the warehouse. |

## Data Source

The report retrieves data from the **Stock Ledger Entry** DocType by:

- Summing `actual_qty` to calculate the current stock balance.
- Summing `stock_value` to determine the total inventory value.
- Grouping results by item and warehouse.
- Excluding records with zero balance quantities.

## Calculation Logic

For each item and warehouse combination:

- **Balance Quantity** = Sum of all `actual_qty`
- **Balance Value** = Sum of all `stock_value`
- **Valuation Rate** = `Balance Value ÷ Balance Quantity`

The report includes only transactions posted on or before the selected **As On Date**.

## Testing

The report includes automated tests to verify:

- Report columns and data are returned successfully.
- Filtering by item.
- Filtering by warehouse.
- Correct calculation of balance quantity, balance value, and valuation rate.
- Correct handling of the **As On Date** filter.

## Related Documents

- [Item](item.md)
- [Warehouse](warehouse.md)
- [Stock Entry](stock_entry.md)
- [Stock Entry Item](stock_entry_item.md)
- [Stock Ledger Entry](stock_ledger_entry.md)
