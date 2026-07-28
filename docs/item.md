# Item DocType

## Overview

The **Item** DocType represents a product or inventory item managed by the warehouse system. It stores the information required to uniquely identify an item, define its unit of measure, and support inventory transactions and reporting.

Each item can participate in stock receipts, consumption, transfers, and inventory reports.

---

## Purpose

The Item DocType is used to:

* Define products managed by the warehouse.
* Provide a unique identifier for inventory transactions.
* Specify the unit of measure used for stock movement.
* Support inventory reporting and stock valuation.
* Maintain item information throughout its lifecycle.

---

## Fields

### Item Code

A unique identifier used to reference the item throughout the system.

**Example:**

* LAP001
* MON001
* KBD001

---

### Item Name

A descriptive name used to identify the item.

**Example:**

* Dell Latitude 7420
* 24-inch Monitor
* Wireless Keyboard

---

### Description

(Optional)

Additional information describing the item, such as specifications or notes.

---

### Unit of Measurement

Specifies the unit used when recording inventory quantities.

**Example:**

* Nos
* Box
* Pack
* Kg

---

### Disabled

Indicates whether the item can be used in new stock transactions.

* **Enabled:** The item is available for inventory operations.
* **Disabled:** The item cannot be used in new stock transactions while historical records remain available.

---

## Related DocTypes

### Warehouse

Represents the locations where items are stored.

### Stock Entry

Records inventory movements involving items.

### Stock Ledger Entry

Maintains the inventory movement history for each item.

---

## Usage

Typical workflow:

1. Create an item.
2. Specify its unit of measure.
3. Receive inventory through a Stock Entry.
4. Transfer or consume inventory as required.
5. View inventory movement using the Stock Ledger report.
6. View current inventory balances using the Stock Balance report.

---

## Best Practices

* Use meaningful and consistent item codes.
* Keep item names descriptive and easy to identify.
* Select the correct unit of measure before recording stock.
* Disable obsolete items instead of deleting them to preserve historical records.
* Update item information when product details change.

---

## Example

| Item Code | Item Name          | UOM | Disabled |
| --------- | ------------------ | --- | :------: |
| LAP001    | Dell Latitude 7420 | Nos |     ✗    |
| MON001    | 24-inch Monitor    | Nos |     ✗    |
| KBD001    | Wireless Keyboard  | Nos |     ✓    |

---

## Notes

* Every stock transaction references an item.
* Inventory balances and valuation are tracked per item.
* Historical transactions remain available even if an item is disabled.

---

## Testing

The Item DocType currently contains metadata and configuration only and does not implement custom server-side business logic. As a result, no dedicated unit tests are required at this stage.

