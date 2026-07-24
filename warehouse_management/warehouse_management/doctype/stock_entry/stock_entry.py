import frappe
from frappe.model.document import Document
from frappe.utils import flt


class StockEntry(Document):
    def validate(self):
        for row in self.items:
            if self.purpose == "Receipt":
                if not row.target_warehouse:
                    frappe.throw(f"Row {row.idx}: Target Warehouse is required for Receipt")
                if not row.rate:
                    frappe.throw(f"Row {row.idx}: Rate is required for Receipt")
            elif self.purpose == "Consume":
                if not row.source_warehouse:
                    frappe.throw(f"Row {row.idx}: Source Warehouse is required for Consume")
            elif self.purpose == "Transfer":
                if not row.source_warehouse or not row.target_warehouse:
                    frappe.throw(f"Row {row.idx}: Both Source and Target Warehouse are required for Transfer")
                if row.source_warehouse == row.target_warehouse:
                    frappe.throw(f"Row {row.idx}: Source and Target Warehouse cannot be the same")

    def on_submit(self):
        for row in self.items:
            if self.purpose == "Receipt":
                self.make_sle(row.item, row.target_warehouse, flt(row.qty), rate=flt(row.rate))
            elif self.purpose == "Consume":
                rate = self.get_current_valuation_rate(row.item, row.source_warehouse)
                self.make_sle(row.item, row.source_warehouse, -flt(row.qty), rate=rate)
            elif self.purpose == "Transfer":
                rate = self.get_current_valuation_rate(row.item, row.source_warehouse)
                self.make_sle(row.item, row.source_warehouse, -flt(row.qty), rate=rate)
                self.make_sle(row.item, row.target_warehouse, flt(row.qty), rate=rate)

    def on_cancel(self):
        # Simplest correct approach for a stateless ledger: reverse with
        # equal-and-opposite entries rather than deleting rows, so the
        # ledger stays a true append-only audit trail.
        for row in self.items:
            if self.purpose == "Receipt":
                self.make_sle(row.item, row.target_warehouse, -flt(row.qty), rate=flt(row.rate))
            elif self.purpose == "Consume":
                rate = self.get_current_valuation_rate(row.item, row.source_warehouse)
                self.make_sle(row.item, row.source_warehouse, flt(row.qty), rate=rate)
            elif self.purpose == "Transfer":
                rate = self.get_current_valuation_rate(row.item, row.source_warehouse)
                self.make_sle(row.item, row.source_warehouse, flt(row.qty), rate=rate)
                self.make_sle(row.item, row.target_warehouse, -flt(row.qty), rate=rate)

    def make_sle(self, item, warehouse, actual_qty, rate):
        sle = frappe.get_doc({
            "doctype": "Stock Ledger Entry",
            "posting_date": self.posting_date,
            "item": item,
            "warehouse": warehouse,
            "actual_qty": actual_qty,
            "valuation_rate": rate,
            "stock_value": flt(actual_qty) * flt(rate),
            "voucher_type": "Stock Entry",
            "voucher_no": self.name,
        })
        sle.insert(ignore_permissions=True)

    def get_current_valuation_rate(self, item, warehouse):
        """
        Moving average rate = running value / running qty,
        computed from existing Stock Ledger Entries up to now.
        This is the 'single SQL query' the assignment mentions.
        """
        result = frappe.db.sql("""
            SELECT
                SUM(actual_qty) as total_qty,
                SUM(stock_value) as total_value
            FROM `tabStock Ledger Entry`
            WHERE item = %s AND warehouse = %s
        """, (item, warehouse), as_dict=True)

        if not result or not result[0].total_qty:
            frappe.throw(
                f"No stock available for Item {item} in Warehouse {warehouse} to consume/transfer from"
            )

        return flt(result[0].total_value) / flt(result[0].total_qty)
