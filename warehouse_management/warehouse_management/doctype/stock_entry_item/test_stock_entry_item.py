# Copyright (c) 2026, App Publisher and Contributors
# See license.txt

import frappe
from frappe.exceptions import ValidationError
from frappe.tests.utils import FrappeTestCase


class TestStockEntryItem(FrappeTestCase):
	"""Tests for Stock Entry Item validation."""

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

	def test_quantity_must_be_greater_than_zero(self):
		"""A Stock Entry Item cannot have a zero or negative quantity."""
		item = self.make_item()

		for qty in (0, -5):
			with self.assertRaises(ValidationError):
				frappe.get_doc(
					{
						"doctype": "Stock Entry Item",
						"item": item.name,
						"qty": qty,
					}
				).insert()
