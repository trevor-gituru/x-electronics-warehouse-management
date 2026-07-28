# Copyright (c) 2026, App Publisher and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	"""Generate the Stock Ledger report."""
	filters = filters or {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	"""Define the columns displayed in the Stock Ledger report."""
	return [
		{
			"label": "Date",
			"fieldname": "posting_date",
			"fieldtype": "Datetime",
			"width": 160,
		},
		{
			"label": "Item",
			"fieldname": "item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 120,
		},
		{
			"label": "Warehouse",
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 120,
		},
		{
			"label": "Qty Change",
			"fieldname": "actual_qty",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": "Valuation Rate",
			"fieldname": "valuation_rate",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"label": "Stock Value Change",
			"fieldname": "stock_value",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": "Voucher Type",
			"fieldname": "voucher_type",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": "Voucher No",
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 140,
		},
	]


def get_data(filters):
	"""Retrieve Stock Ledger entries that match the selected filters."""
	# Build SQL conditions from the selected report filters.
	conditions, values = get_conditions(filters)

	query = f"""
		SELECT
			posting_date,
			item,
			warehouse,
			actual_qty,
			valuation_rate,
			stock_value,
			voucher_type,
			voucher_no
		FROM `tabStock Ledger Entry`
		WHERE {conditions}
		ORDER BY posting_date ASC, creation ASC
	"""

	return frappe.db.sql(query, values, as_dict=True)


def get_conditions(filters):
	"""Build SQL WHERE conditions from the selected report filters."""
	# Start with a condition that always evaluates to true.
	conditions = ["1=1"]
	values = {}

	# Optionally filter by item.
	if filters.get("item"):
		conditions.append("item = %(item)s")
		values["item"] = filters["item"]

	# Optionally filter by warehouse.
	if filters.get("warehouse"):
		conditions.append("warehouse = %(warehouse)s")
		values["warehouse"] = filters["warehouse"]

	# Optionally filter by the start date.
	if filters.get("from_date"):
		conditions.append("posting_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]

	# Optionally filter by the end date.
	if filters.get("to_date"):
		conditions.append("posting_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	return " AND ".join(conditions), values
