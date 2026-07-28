````md id="stock_ledger_entry_docs"
# Stock Ledger Entry DocType

## Overview

The **Stock Ledger Entry** DocType stores the history of all inventory movements within the warehouse management system.

Each entry represents a single stock change for an item in a specific warehouse. Stock Ledger Entries are created automatically from submitted Stock Entries and provide an immutable audit trail of inventory changes.

---

## Purpose

The Stock Ledger Entry DocType is used to:

* Maintain a complete history of inventory movements.
* Track increases and decreases in stock quantities.
* Store inventory valuation information.
* Link stock movements back to their source transactions.
* Support inventory reports such as stock balance and stock movement history.

---

## Fields

### Posting Date

The date when the inventory movement was recorded.

---

### Item

The item affected by the stock movement.

**Example:**

* Laptop
* Keyboard
* Monitor

---

### Warehouse

The warehouse where the inventory movement occurred.

---

### Actual Quantity

The quantity change caused by the stock movement.

* Positive values increase inventory.
* Negative values decrease inventory.

**Examples:**

| Movement | Quantity |
|---|---:|
| Receipt | +10 |
| Consume | -5 |
| Transfer from warehouse | -10 |
| Transfer to warehouse | +10 |

---

### Valuation Rate

The cost per unit used to calculate the inventory value of the movement.

The rate is determined using the current inventory valuation method.

---

### Stock Value

The total inventory value affected by the movement.

Calculation:

```text
Stock Value = Actual Quantity × Valuation Rate
````

---

### Voucher Type

Identifies the document that created the stock ledger entry.

Currently supported:

```text
Stock Entry
```

---

### Voucher Number

Stores the reference number of the source document that generated the ledger entry.

Example:

```text
STE-2026-00001
```

---

## Relationship With Other DocTypes

The Stock Ledger Entry is created from a submitted **Stock Entry**.

Relationship:

```text
Stock Entry
    |
    | contains
    ↓
Stock Entry Item
    |
    | creates
    ↓
Stock Ledger Entry
```

Example:

```text
Stock Entry
Purpose: Receipt

Items:
- Laptop
  Quantity: 10
  Target Warehouse: Main Store

        ↓ Submit

Stock Ledger Entry

Item: Laptop
Warehouse: Main Store
Actual Quantity: +10
```

---

## Stock Movement Flow

### Receipt

Adds inventory to a warehouse.

```text
Stock Entry
    |
    ↓
Stock Ledger Entry

Quantity: positive
Warehouse: target warehouse
```

---

### Consume

Removes inventory from a warehouse.

```text
Stock Entry
    |
    ↓
Stock Ledger Entry

Quantity: negative
Warehouse: source warehouse
```

---

### Transfer

Creates two ledger records:

```text
Source Warehouse
Quantity: negative

Target Warehouse
Quantity: positive
```

Example:

```text
Main Store       -10
Branch Store     +10
```

---

## Naming

Stock Ledger Entries use script-based naming.

Example generated names:

```text
a83fd92bc1
7b29fa102e
```

Ledger names are system-generated because users do not manually create or manage ledger records.

---

## Permissions

Stock Ledger Entries are read-only records.

Users can:

* View ledger history.
* Use ledger data for reports.
* Export ledger information if permitted.

Users cannot:

* Manually edit entries.
* Rename entries.
* Delete entries.

---

## Usage

Typical workflow:

1. User creates a Stock Entry.
2. User adds Stock Entry Items.
3. User submits the Stock Entry.
4. The system creates Stock Ledger Entries automatically.
5. Reports use ledger entries to calculate inventory balances.

---

## Best Practices

* Never modify existing Stock Ledger Entries manually.
* Always create inventory changes through Stock Entry.
* Keep ledger records as an audit history.
* Use voucher references to trace inventory changes back to their source.

---

## Testing

The Stock Ledger Entry tests verify that:

* Ledger entries can be created successfully.
* Names are generated automatically.
* Positive and negative quantity movements are stored correctly.

```
```

