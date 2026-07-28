# Warehouse DocType

## Overview

The **Warehouse** DocType represents a physical or logical location where inventory is stored. Warehouses are used to organize stock, track inventory levels, and facilitate inventory movements such as receipts, consumption, and transfers.

Warehouses support a hierarchical (tree) structure, allowing organizations to group warehouses by company, region, branch, building, or storage area while maintaining a clear inventory structure.

---

## Purpose

The Warehouse DocType is used to:

* Define locations where inventory is stored.
* Support stock receipts, consumption, and transfers.
* Organize warehouses using a parent-child hierarchy.
* Enable inventory reporting by warehouse.
* Track stock quantities and values for each storage location.
* Simplify warehouse management for organizations with multiple storage locations.

---

## Fields

### Warehouse Name

A unique, descriptive name used to identify the warehouse throughout the system.

**Examples:**

* Company Warehouse
* Main Store
* Branch Store
* Finished Goods Warehouse

---

### Parent Warehouse

(Optional)

Specifies the parent warehouse in the warehouse hierarchy.

Only warehouses marked as **Group** warehouses can be selected as parents.

**Example:**

```text
Company Warehouse
├── Main Store
├── Branch Store
└── Cold Storage
```

---

### Is Group

Determines whether the warehouse acts as a grouping node.

* **Enabled**

  * Used only to organize child warehouses.
  * Cannot directly store inventory.
  * Can be selected as a parent warehouse.

* **Disabled**

  * Represents an operational warehouse.
  * Can store inventory and participate in stock transactions.

A warehouse that already has child warehouses cannot be changed to a non-group warehouse until its children are removed or reassigned.

---

### Disabled

Marks the warehouse as inactive.

When disabled:

* The warehouse is unavailable for new stock transactions.
* Historical stock records remain available for reporting and auditing.
* Existing references to the warehouse are preserved.

This allows warehouses to be retired without deleting historical inventory data.

---

## Warehouse Hierarchy

Warehouses are organized as a tree structure.

Example:

```text
Company Warehouse
├── Main Store
├── Branch Store
│   ├── Shelf A
│   └── Shelf B
└── Transit Warehouse
```

This hierarchy makes it easier to organize warehouses while keeping inventory separated by location.

---

## Validation Rules

The Warehouse DocType enforces the following business rules:

* Only **Group** warehouses can be selected as parent warehouses.
* A warehouse with child warehouses must remain marked as a **Group** warehouse.
* Inventory should only be stored in non-group warehouses.
* Disabled warehouses should not be used for new stock transactions.

These validations help maintain a consistent warehouse hierarchy and prevent invalid inventory structures.

---

## Related DocTypes

### Item

Represents products stored within warehouses.

### Stock Entry

Records inventory movements such as receipts, consumption, and transfers.

### Stock Ledger Entry

Stores the complete history of stock movements affecting each warehouse.

---

## Testing

Automated unit tests are provided to verify the Warehouse DocType's custom validation logic, hierarchical behavior, and business rules. The test suite ensures warehouse operations behave as expected and helps prevent regressions when the implementation is modified.

Run the tests using:

```bash
bench --site <site-name> run-tests \
    --module warehouse_management.warehouse_management.doctype.warehouse.test_warehouse
```


## Usage

Typical workflow:

1. Create one or more warehouses.
2. Create group warehouses to organize storage locations.
3. Create operational warehouses beneath the appropriate group warehouses.
4. Receive inventory into a warehouse using a Stock Entry.
5. Transfer inventory between warehouses.
6. Consume inventory from a warehouse.
7. Review inventory using the Stock Balance and Stock Ledger reports.

---

## Best Practices

* Use descriptive and meaningful warehouse names.
* Keep warehouse names unique.
* Organize warehouses using parent group warehouses.
* Reserve **Group** warehouses for organizational purposes only.
* Store inventory only in non-group warehouses.
* Disable warehouses instead of deleting them to preserve inventory history.

---

## Example

| Warehouse         | Parent            | Is Group | Disabled |
| ----------------- | ----------------- | :------: | :------: |
| Company Warehouse | —                 |     ✓    |     ✗    |
| Main Store        | Company Warehouse |     ✗    |     ✗    |
| Branch Store      | Company Warehouse |     ✗    |     ✗    |
| Shelf A           | Branch Store      |     ✗    |     ✗    |
| Closed Warehouse  | Company Warehouse |     ✗    |     ✓    |

---

## Notes

* Every stock movement references one or more warehouses.
* Inventory balances are maintained independently for each warehouse.
* Stock Balance and Stock Ledger reports summarize inventory using warehouse data.
* Group warehouses organize child warehouses and are not intended to hold inventory directly.

