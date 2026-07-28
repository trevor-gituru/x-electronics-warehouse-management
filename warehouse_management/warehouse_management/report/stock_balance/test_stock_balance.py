import frappe
from frappe.tests.utils import FrappeTestCase

from warehouse_management.warehouse_management.report.stock_balance.stock_balance import (
	execute,
)


class TestStockBalanceReport(FrappeTestCase):
	"""Tests for the Stock Balance report."""

	def setUp(self):
		"""Create test data used by all report test cases."""
		self.item_code = "TEST-BAL-ITEM"
		self.warehouse = "Test Balance Warehouse"

		# Create a test item if it does not already exist.
		if not frappe.db.exists("Item", self.item_code):
			frappe.get_doc(
				{
					"doctype": "Item",
					"item_code": self.item_code,
					"item_name": "Test Balance Item",
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

		# Create and submit a stock receipt:
		# 10 units @ 100 = 1000 total value.
		receipt = frappe.get_doc(
			{
				"doctype": "Stock Entry",
				"purpose": "Receipt",
				"items": [
					{
						"item": self.item_code,
						"qty": 10,
						"rate": 100,
						"target_warehouse": self.warehouse,
					}
				],
			}
		)
		receipt.insert()
		receipt.submit()

	def tearDown(self):
		"""Rollback database changes after each test."""
		frappe.db.rollback()

	def test_report_returns_columns_and_data(self):
		"""The report should return both column definitions and data."""
		columns, data = execute({})

		self.assertTrue(len(columns) > 0)
		self.assertTrue(len(data) > 0)

	def test_report_filters_by_item(self):
		"""The report should only return records for the selected item."""
		_, data = execute({"item": self.item_code})

		self.assertGreater(len(data), 0)
		self.assertTrue(all(row["item"] == self.item_code for row in data))

	def test_report_filters_by_warehouse(self):
		"""The report should only return records for the selected warehouse."""
		_, data = execute({"warehouse": self.warehouse})

		self.assertGreater(len(data), 0)
		self.assertTrue(all(row["warehouse"] == self.warehouse for row in data))

	def test_report_shows_correct_balance(self):
		"""The report should calculate the correct quantity, value, and valuation rate."""
		_, data = execute(
			{
				"item": self.item_code,
				"warehouse": self.warehouse,
			}
		)

		self.assertEqual(len(data), 1)

		row = data[0]

		self.assertEqual(row["balance_qty"], 10)
		self.assertEqual(row["balance_value"], 1000)
		self.assertEqual(row["valuation_rate"], 100)

	def test_report_as_on_date_excludes_future_entries(self):
		"""The report should exclude entries posted after the selected date."""
		_, data = execute(
			{
				"item": self.item_code,
				"warehouse": self.warehouse,
				"as_on_date": "2000-01-01",
			}
		)

		self.assertEqual(len(data), 0)
