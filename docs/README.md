# Warehouse Management Documentation

This directory contains documentation for the Warehouse Management application, including DocTypes, inventory workflows, and system behavior.

## Overview

The Warehouse Management system provides functionality for managing:

- Items and item information.
- Warehouse locations and hierarchy.
- Stock movements through receipts, consumption, and transfers.
- Inventory history and valuation tracking.

## DocTypes

### Item

Represents products managed within the inventory system.

Documentation:

[Item DocType](item.md)

---

### Warehouse

Represents physical or logical storage locations where inventory is managed.

Supports:

- Warehouse hierarchy.
- Parent-child warehouse relationships.
- Group warehouses for organization.

Documentation:

[Warehouse DocType](warehouse.md)

---

### Stock Entry

Records inventory transactions such as:

- Receipt of stock.
- Consumption of stock.
- Transfer between warehouses.

A submitted Stock Entry creates corresponding Stock Ledger Entries.

Documentation:

[Stock Entry DocType](stock_entry.md)

---

### Stock Entry Item

Represents individual item rows within a Stock Entry.

Stores:

- Item.
- Quantity.
- Rate.
- Source warehouse.
- Target warehouse.

Documentation:

[Stock Entry Item DocType](stock_entry_item.md)

---

### Stock Ledger Entry

Stores the historical record of inventory movements.

Tracks:

- Quantity changes.
- Inventory valuation.
- Warehouse movements.
- Source transaction references.

Documentation:

[Stock Ledger Entry DocType](stock_ledger_entry.md)

---

## Inventory Flow

The general inventory process is:

```text
Item
 |
 |
Stock Entry
 |
 | contains
 ↓
Stock Entry Item
 |
 | submit
 ↓
Stock Ledger Entry

---

## Reports

### Stock Balance Report

Displays the current inventory balance for each item and warehouse by summarizing Stock Ledger Entries up to a selected date.

Supports:

- Stock quantity balances.
- Inventory valuation.
- Filtering by item.
- Filtering by warehouse.
- Historical "As On Date" reporting.

Documentation:

[Stock Balance Report](stock_balance.md)
