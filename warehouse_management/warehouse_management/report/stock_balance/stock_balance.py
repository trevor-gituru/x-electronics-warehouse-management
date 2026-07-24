# Copyright (c) 2026, App Publisher and contributors
# For license information, please see license.txt
import frappe
from frappe.utils import nowdate


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": "Item",
			"fieldname": "item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{
			"label": "Warehouse",
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 150,
		},
		{
			"label": "Balance Qty",
			"fieldname": "balance_qty",
			"fieldtype": "Float",
			"width": 120,
		},
		{
			"label": "Valuation Rate",
			"fieldname": "valuation_rate",
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"label": "Balance Value",
			"fieldname": "balance_value",
			"fieldtype": "Currency",
			"width": 140,
		},
	]


def get_data(filters):
	as_on_date = filters.get("as_on_date") or nowdate()
	conditions, values = get_conditions(filters, as_on_date)

	query = f"""
        SELECT
            item,
            warehouse,
            SUM(actual_qty) as balance_qty,
            SUM(stock_value) as balance_value
        FROM `tabStock Ledger Entry`
        WHERE {conditions}
        GROUP BY item, warehouse
        HAVING SUM(actual_qty) != 0
        ORDER BY item, warehouse
    """
	rows = frappe.db.sql(query, values, as_dict=True)

	for row in rows:
		row["valuation_rate"] = row["balance_value"] / row["balance_qty"] if row["balance_qty"] else 0

	return rows


def get_conditions(filters, as_on_date):
	conditions = ["posting_date <= %(as_on_date)s"]
	values = {"as_on_date": as_on_date}

	if filters.get("item"):
		conditions.append("item = %(item)s")
		values["item"] = filters["item"]

	if filters.get("warehouse"):
		conditions.append("warehouse = %(warehouse)s")
		values["warehouse"] = filters["warehouse"]

	return " AND ".join(conditions), values
