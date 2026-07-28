# Stock Entry DocType

## Overview

The **Stock Entry** DocType represents an inventory transaction that records the movement of stock into, out of, or between warehouses. It acts as the primary transaction document from which inventory movements are processed and recorded in the Stock Ledger.

A Stock Entry may contain one or more items, allowing multiple inventory movements to be recorded as a single transaction.

---

## Purpose

The Stock Entry DocType is used to:

* Record inventory receipts.
* Record inventory consumption.
* Transfer inventory between warehouses.
* Generate Stock Ledger Entries that update inventory balances.
* Provide an auditable record of inventory transactions.

---

## Stock Entry Workflow

A Stock Entry records the intended inventory movement. When the document is submitted, the system automatically creates one or more **Stock Ledger Entries** for each item in the transaction.

```text
Stock Entry
        │
        ▼
Stock Entry Items
        │
        ▼
Stock Ledger Entries
        │
        ▼
Stock Balance & Stock Ledger Reports
```

---

## Purpose Types

### Receipt

Records inventory received into a warehouse.

Example:

```text
Supplier
      │
      ▼
Main Warehouse
```

Creates one positive Stock Ledger Entry.

---

### Consume

Records inventory removed from a warehouse.

Example:

```text
Main Warehouse
      │
      ▼
Production / Usage
```

Creates one negative Stock Ledger Entry.

---

### Transfer

Moves inventory from one warehouse to another.

Example:

```text
Main Warehouse
      │
      ▼
Branch Warehouse
```

Creates:

* One negative Stock Ledger Entry for the source warehouse.
* One positive Stock Ledger Entry for the target warehouse.

---

## Fields

### Naming Series

Defines the numbering format used to generate the Stock Entry identifier automatically.

---

### Purpose

Specifies the type of inventory movement being recorded.

Available options:

* Receipt
* Consume
* Transfer

---

### Posting Date

The date on which the stock movement takes effect in the inventory records.

---

### Items

Contains the items involved in the stock movement, including quantities, valuation rates, and source or target warehouses.

A single Stock Entry may contain multiple item rows.

---

### Remarks

Optional notes or comments providing additional context for the transaction.

---

## Related DocTypes

### Stock Entry Item

Stores the individual items that make up the Stock Entry.

### Stock Ledger Entry

Records the inventory movements generated when a Stock Entry is submitted.

### Item

Represents the products involved in the transaction.

### Warehouse

Represents the warehouses participating in the stock movement.

---

## Validation Rules

The Stock Entry validates its data before submission.

Depending on the selected purpose:

### Receipt

* Target Warehouse is required.
* Valuation Rate is required.

### Consume

* Source Warehouse is required.

### Transfer

* Source Warehouse is required.
* Target Warehouse is required.
* Source and Target warehouses must be different.

---

## Submission

Submitting a Stock Entry generates one or more Stock Ledger Entries.

The Stock Entry itself does not store inventory balances. Instead, inventory quantities and values are derived from the generated Stock Ledger Entries.

---

## Cancellation

Cancelling a submitted Stock Entry does not remove Stock Ledger Entries.

Instead, the system creates equal and opposite Stock Ledger Entries to reverse the original inventory movement while preserving a complete audit trail.

---

## Usage

Typical workflow:

1. Create a Stock Entry.
2. Select the inventory movement purpose.
3. Add one or more items.
4. Specify the appropriate source or target warehouses.
5. Submit the document.
6. The system generates Stock Ledger Entries automatically.
7. View inventory changes using the Stock Ledger and Stock Balance reports.

---

## Best Practices

* Group related inventory movements into a single Stock Entry.
* Verify warehouse selections before submitting.
* Ensure valuation rates are provided for receipts.
* Use remarks to document the reason for the transaction.
* Avoid cancelling submitted entries unless a correction is required.

---

## Example

| Stock Entry | Purpose  | Item   | Quantity |
| ----------- | -------- | ------ | -------: |
| STE-00001   | Receipt  | Laptop |       10 |
| STE-00002   | Transfer | Laptop |        5 |
| STE-00003   | Consume  | Laptop |        2 |

---

## Notes

* A single Stock Entry may contain multiple Stock Entry Items.
* Each Stock Entry Item generates one or more Stock Ledger Entries depending on the transaction type.
* Inventory reports derive their balances from Stock Ledger Entries rather than directly from Stock Entries.

---

## Testing

Automated unit tests verify Stock Entry validation rules, stock movement processing, Stock Ledger Entry generation, cancellation behavior, and valuation calculations.

Run the tests using:

```bash
bench --site <site-name> run-tests \
    --module warehouse_management.warehouse_management.doctype.stock_entry.test_stock_entry
```

