import frappe
from frappe.tests.utils import FrappeTestCase

from warehouse_management.warehouse_management.report.stock_ledger.stock_ledger import (
	execute,
)


class TestStockLedgerReport(FrappeTestCase):
	"""Tests for the Stock Ledger report."""

	def setUp(self):
		"""Create test data used by all Stock Ledger report test cases."""
		self.item_code = "TEST-RPT-ITEM"
		self.warehouse = "Test Report Warehouse"

		# Create a test item if it does not already exist.
		if not frappe.db.exists("Item", self.item_code):
			frappe.get_doc(
				{
					"doctype": "Item",
					"item_code": self.item_code,
					"item_name": "Test Report Item",
					"uom": "Nos",
				}
			).insert()

		# Create a test warehouse if it does not already exist.
		if not frappe.db.exists("Warehouse", self.warehouse):
			frappe.get_doc(
				{
					"doctype": "Warehouse",
					"warehouse_name": self.warehouse,
				}
			).insert()

		# Create and submit a stock receipt so the report has ledger data.
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
		"""Rollback database changes after each test."""
		frappe.db.rollback()

	def test_report_returns_columns_and_data(self):
		"""The report should return both column definitions and ledger data."""
		columns, data = execute({})

		self.assertTrue(len(columns) > 0)
		self.assertTrue(len(data) > 0)

	def test_report_filters_by_item(self):
		"""The report should only return entries for the selected item."""
		_, data = execute({"item": self.item_code})

		self.assertTrue(all(row["item"] == self.item_code for row in data))

	def test_report_filters_by_warehouse(self):
		"""The report should only return entries for the selected warehouse."""
		_, data = execute({"warehouse": self.warehouse})

		self.assertTrue(all(row["warehouse"] == self.warehouse for row in data))

	def test_report_shows_correct_values(self):
		"""The report should return the correct ledger values for the stock movement."""
		_, data = execute(
			{
				"item": self.item_code,
				"warehouse": self.warehouse,
			}
		)

		row = data[0]

		self.assertEqual(row["actual_qty"], 5)
		self.assertEqual(row["valuation_rate"], 100)
		self.assertEqual(row["stock_value"], 500)
		self.assertEqual(row["voucher_no"], self.receipt.name)

	def test_report_date_filter_excludes_old_entries(self):
		"""The report should exclude entries posted before the selected start date."""
		_, data = execute(
			{
				"item": self.item_code,
				"from_date": "2099-01-01",
			}
		)

		self.assertEqual(len(data), 0)
