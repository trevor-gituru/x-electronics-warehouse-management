# Copyright (c) 2026, App Publisher and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestStockLedgerEntry(FrappeTestCase):
    """Tests for Stock Ledger Entry creation and naming."""

    def make_item(self):
        """Create and return a test item."""
        item_code = f"ITEM-{frappe.generate_hash(length=8)}"

        return frappe.get_doc(
            {
                "doctype": "Item",
                "item_code": item_code,
                "item_name": item_code,
                "uom": "Nos",
            }
        ).insert()

    def make_warehouse(self):
        """Create and return a test warehouse."""
        warehouse_name = f"WH-{frappe.generate_hash(length=8)}"

        return frappe.get_doc(
            {
                "doctype": "Warehouse",
                "warehouse_name": warehouse_name,
            }
        ).insert()

    def test_stock_ledger_entry_generates_name(self):
        """Stock Ledger Entry should generate a unique name automatically."""
        item = self.make_item()
        warehouse = self.make_warehouse()

        sle = frappe.get_doc(
            {
                "doctype": "Stock Ledger Entry",
                "posting_date": "2026-07-28",
                "item": item.name,
                "warehouse": warehouse.name,
                "actual_qty": 10,
                "valuation_rate": 100,
                "stock_value": 1000,
                "voucher_type": "Stock Entry",
                "voucher_no": "STE-TEST-001",
            }
        ).insert()

        self.assertTrue(sle.name)
        self.assertEqual(sle.actual_qty, 10)
        self.assertEqual(sle.stock_value, 1000)

    def test_stock_ledger_entry_stores_negative_quantity(self):
        """Stock Ledger Entry should allow negative quantities for stock reduction."""
        item = self.make_item()
        warehouse = self.make_warehouse()

        sle = frappe.get_doc(
            {
                "doctype": "Stock Ledger Entry",
                "posting_date": "2026-07-28",
                "item": item.name,
                "warehouse": warehouse.name,
                "actual_qty": -5,
                "valuation_rate": 100,
                "stock_value": -500,
                "voucher_type": "Stock Entry",
                "voucher_no": "STE-TEST-002",
            }
        ).insert()

        self.assertEqual(sle.actual_qty, -5)
        self.assertEqual(sle.stock_value, -500)
