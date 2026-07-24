import frappe
from frappe.tests.utils import FrappeTestCase
from warehouse_management.warehouse_management.report.stock_ledger.stock_ledger import (
    execute,
)


class TestStockLedgerReport(FrappeTestCase):
    def setUp(self):
        self.item_code = "TEST-RPT-ITEM"
        self.warehouse = "Test Report Warehouse"

        if not frappe.db.exists("Item", self.item_code):
            frappe.get_doc(
                {
                    "doctype": "Item",
                    "item_code": self.item_code,
                    "item_name": "Test Report Item",
                    "uom": "Nos",
                }
            ).insert()

        if not frappe.db.exists("Warehouse", self.warehouse):
            frappe.get_doc(
                {
                    "doctype": "Warehouse",
                    "warehouse_name": self.warehouse,
                }
            ).insert()

        # Create one Receipt so the ledger has data to report on
        receipt = frappe.get_doc(
            {
                "doctype": "Stock Entry",
                "purpose": "Receipt",
                "items": [
                    {
                        "item": self.item_code,
                        "qty": 5,
                        "rate": 100,
                        "target_warehouse": self.warehouse,
                    }
                ],
            }
        )
        receipt.insert()
        receipt.submit()
        self.receipt = receipt

    def tearDown(self):
        frappe.db.rollback()

    def test_report_returns_columns_and_data(self):
        columns, data = execute({})
        self.assertTrue(len(columns) > 0)
        self.assertTrue(len(data) > 0)

    def test_report_filters_by_item(self):
        columns, data = execute({"item": self.item_code})
        self.assertTrue(all(row["item"] == self.item_code for row in data))

    def test_report_filters_by_warehouse(self):
        columns, data = execute({"warehouse": self.warehouse})
        self.assertTrue(all(row["warehouse"] == self.warehouse for row in data))

    def test_report_shows_correct_values(self):
        columns, data = execute({"item": self.item_code, "warehouse": self.warehouse})
        row = data[0]
        self.assertEqual(row["actual_qty"], 5)
        self.assertEqual(row["valuation_rate"], 100)
        self.assertEqual(row["stock_value"], 500)
        self.assertEqual(row["voucher_no"], self.receipt.name)

    def test_report_date_filter_excludes_old_entries(self):
        # A from_date far in the future should return nothing
        columns, data = execute(
            {
                "item": self.item_code,
                "from_date": "2099-01-01",
            }
        )
        self.assertEqual(len(data), 0)
