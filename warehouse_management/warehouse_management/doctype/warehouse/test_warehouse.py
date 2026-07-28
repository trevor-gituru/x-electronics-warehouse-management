# Copyright (c) 2026, App Publisher and Contributors
# See license.txt

import frappe
from frappe.exceptions import ValidationError
from frappe.tests.utils import FrappeTestCase


class TestWarehouse(FrappeTestCase):
    """Tests for Warehouse DocType validation rules."""

    def make_warehouse(self, is_group=False, parent=None):
        """Create and return a warehouse with a unique name."""
        warehouse_name = f"WH-{frappe.generate_hash(length=8)}"

        return frappe.get_doc(
            {
                "doctype": "Warehouse",
                "warehouse_name": warehouse_name,
                "is_group": is_group,
                "parent_warehouse": parent,
            }
        ).insert()

    def test_group_warehouse_can_be_parent(self):
        """A warehouse marked as a group can be assigned as a parent."""
        parent = self.make_warehouse(is_group=True)

        child = self.make_warehouse(parent=parent.name)

        self.assertEqual(child.parent_warehouse, parent.name)

    def test_non_group_warehouse_cannot_be_parent(self):
        """A non-group warehouse cannot be assigned as a parent."""
        parent = self.make_warehouse(is_group=False)

        with self.assertRaises(ValidationError):
            self.make_warehouse(parent=parent.name)

    def test_group_with_children_cannot_become_non_group(self):
        """A warehouse with child warehouses must remain a group."""
        parent = self.make_warehouse(is_group=True)

        self.make_warehouse(parent=parent.name)

        parent.is_group = 0

        with self.assertRaises(ValidationError):
            parent.save()

    def test_group_without_children_can_become_non_group(self):
        """A group warehouse without children can be converted to a non-group warehouse."""
        warehouse = self.make_warehouse(is_group=True)

        warehouse.is_group = 0
        warehouse.save()

        self.assertFalse(warehouse.is_group)

    def test_root_warehouse_can_be_created(self):
        """A warehouse without a parent should be created successfully."""
        warehouse = self.make_warehouse()

        self.assertIsNone(warehouse.parent_warehouse)
