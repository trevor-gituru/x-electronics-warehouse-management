## Stock Ledger Report

The **Stock Ledger Report** provides a chronological view of all inventory movements recorded in the Stock Ledger Entry DocType. It enables users to audit stock transactions, trace inventory history, and review quantity and valuation changes for each item.

### Purpose

The report helps users:

- View all stock movements in chronological order.
- Track inventory changes for individual items.
- Monitor stock activity within specific warehouses.
- Review valuation rates and stock value changes.
- Trace transactions back to their originating Stock Entry.

### Filters

The report supports the following filters:

- **Item** – Display ledger entries for a specific item.
- **Warehouse** – Display entries for a specific warehouse.
- **From Date** – Show entries posted on or after the selected date.
- **To Date** – Show entries posted on or before the selected date.

### Report Columns

The report displays the following information:

| Column | Description |
|---------|-------------|
| Date | Posting date of the inventory transaction. |
| Item | Item involved in the stock movement. |
| Warehouse | Warehouse where the transaction occurred. |
| Qty Change | Quantity added to or removed from inventory. |
| Valuation Rate | Cost per unit at the time of the transaction. |
| Stock Value Change | Monetary value added to or removed from inventory. |
| Voucher Type | Source document type that created the ledger entry. |
| Voucher No | Reference to the originating transaction document. |

### Data Source

The report retrieves data from the **Stock Ledger Entry** DocType. Results are ordered by posting date and creation time to preserve the sequence of inventory transactions.

### Testing

Automated tests verify that the report:

- Returns column definitions and ledger data.
- Filters correctly by item.
- Filters correctly by warehouse.
- Applies date range filters correctly.
- Displays the correct quantity, valuation rate, stock value, and voucher reference.
