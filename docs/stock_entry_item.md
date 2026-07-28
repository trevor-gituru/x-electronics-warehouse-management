# Stock Entry Item DocType

## Overview

The **Stock Entry Item** DocType is a child table of **Stock Entry** that stores the individual items involved in an inventory transaction. Each row represents a single item being received, consumed, or transferred.

Users do not create Stock Entry Item records directly. Instead, they are automatically created when items are added to the **Items** table of a Stock Entry.

---

## Purpose

The Stock Entry Item DocType is used to:

* Record the individual items included in a Stock Entry.
* Specify quantities and valuation rates for each item.
* Identify the source and target warehouses involved in the movement.
* Provide the information required to generate Stock Ledger Entries.

---

## Relationship

Each **Stock Entry** can contain one or more **Stock Entry Items**.

```text
Stock Entry
      │
      ├── Stock Entry Item
      ├── Stock Entry Item
      └── Stock Entry Item
```

When a Stock Entry is submitted, each Stock Entry Item generates one or more **Stock Ledger Entries** depending on the transaction purpose.

---

## Fields

### Item

The inventory item included in the stock movement.

---

### Quantity

The quantity of the item being received, consumed, or transferred.

The quantity must be greater than zero.

---

### Rate

The valuation rate per unit used to calculate the inventory value. This field is required for receipt transactions.

---

### Source Warehouse

The warehouse from which the item is consumed or transferred.

Required for:

* Consume
* Transfer

---

### Target Warehouse

The warehouse to which the item is received or transferred.

Required for:

* Receipt
* Transfer

---

## Validation

The Stock Entry Item validates that:

* Quantity is greater than zero.

Additional validation, such as required warehouses and transaction-specific rules, is performed by the parent **Stock Entry** DocType.

---

## Usage

Typical workflow:

1. Create a Stock Entry.
2. Add one or more rows to the **Items** table.
3. Select the item and quantity.
4. Specify the appropriate source or target warehouse based on the transaction purpose.
5. Submit the Stock Entry.
6. The system generates the corresponding Stock Ledger Entries.

---

## Best Practices

* Use a positive quantity for every item.
* Verify the selected warehouses before submitting the Stock Entry.
* Provide an accurate valuation rate for receipt transactions.
* Group related items into a single Stock Entry whenever possible.

---

## Example

| Item   | Quantity |   Rate | Source         | Target           |
| ------ | -------: | -----: | -------------- | ---------------- |
| Laptop |       10 | 850.00 | —              | Main Warehouse   |
| Laptop |        2 |      — | Main Warehouse | —                |
| Laptop |        5 |      — | Main Warehouse | Branch Warehouse |

---

## Notes

* Stock Entry Item is a child DocType and cannot exist independently of a Stock Entry.
* Each row represents a single inventory movement within a Stock Entry.
* Stock Ledger Entries are generated from Stock Entry Items when the parent Stock Entry is submitted.

---

## Testing

Automated unit tests verify Stock Entry Item validation, including ensuring that item quantities are greater than zero.

