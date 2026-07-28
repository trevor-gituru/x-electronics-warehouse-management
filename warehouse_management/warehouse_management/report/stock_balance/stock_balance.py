# Copyright (c) 2026, App Publisher and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import nowdate


def execute(filters=None):
	"""Generate the Stock Balance report."""
	filters = filters or {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	"""Define the columns displayed in the Stock Balance report."""
	return [
		{
			"label": _("Item"),
			"fieldname": "item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 150,
		},
		{
			"label": _("Balance Qty"),
			"fieldname": "balance_qty",
			"fieldtype": "Float",
			"width": 120,
		},
		{
			"label": _("Valuation Rate"),
			"fieldname": "valuation_rate",
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"label": _("Balance Value"),
			"fieldname": "balance_value",
			"fieldtype": "Currency",
			"width": 140,
		},
	]


def get_data(filters):
	"""Retrieve stock balances grouped by item and warehouse."""
	# Use today's date if no reporting date is provided.
	as_on_date = filters.get("as_on_date") or nowdate()

	# Build SQL conditions based on the selected filters.
	conditions, values = get_conditions(filters, as_on_date)

	query = (
		"""
		SELECT
			item,
			warehouse,
			SUM(actual_qty) AS balance_qty,
			SUM(stock_value) AS balance_value
		FROM `tabStock Ledger Entry`
		WHERE """
		+ conditions
		+ """
		GROUP BY item, warehouse
		HAVING SUM(actual_qty) != 0
		ORDER BY item, warehouse
	"""
	)

	rows = frappe.db.sql(query, values=values, as_dict=True)

	# Calculate the moving average valuation rate for each stock balance.
	for row in rows:
		row["valuation_rate"] = row["balance_value"] / row["balance_qty"] if row["balance_qty"] else 0

	return rows


def get_conditions(filters, as_on_date):
	"""Build SQL WHERE conditions from the selected report filters."""
	# Always filter by the selected reporting date.
	conditions = ["posting_date <= %(as_on_date)s"]
	values = {"as_on_date": as_on_date}

	# Optionally filter by item.
	if filters.get("item"):
		conditions.append("item = %(item)s")
		values["item"] = filters["item"]

	# Optionally filter by warehouse.
	if filters.get("warehouse"):
		conditions.append("warehouse = %(warehouse)s")
		values["warehouse"] = filters["warehouse"]

	return " AND ".join(conditions), values
