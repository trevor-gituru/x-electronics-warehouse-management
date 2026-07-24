import frappe
from frappe.tests.utils import FrappeTestCase


class TestStockEntry(FrappeTestCase):
	def setUp(self):
		self.item_code = "TEST-LAP-001"
		self.warehouse_1 = "Test Main Store"
		self.warehouse_2 = "Test Branch Store"

		if not frappe.db.exists("Item", self.item_code):
			frappe.get_doc(
				{
					"doctype": "Item",
					"item_code": self.item_code,
					"item_name": "Test Laptop",
					"uom": "Nos",
				}
			).insert()

		for wh in (self.warehouse_1, self.warehouse_2):
			if not frappe.db.exists("Warehouse", wh):
				frappe.get_doc(
					{
						"doctype": "Warehouse",
						"warehouse_name": wh,
					}
				).insert()

	def tearDown(self):
		frappe.db.rollback()

	def make_stock_entry(self, purpose, qty, rate=None, source=None, target=None, submit=True):
		row = {"item": self.item_code, "qty": qty}
		if rate is not None:
			row["rate"] = rate
		if source is not None:
			row["source_warehouse"] = source
		if target is not None:
			row["target_warehouse"] = target

		doc = frappe.get_doc(
			{
				"doctype": "Stock Entry",
				"purpose": purpose,
				"items": [row],
			}
		)
		doc.insert()
		if submit:
			doc.submit()
		return doc

	def get_sles(self, voucher_no):
		return frappe.get_all(
			"Stock Ledger Entry",
			filters={"voucher_no": voucher_no},
			fields=["item", "warehouse", "actual_qty", "valuation_rate", "stock_value"],
			order_by="creation",
		)

	# ---------- Receipt ----------

	def test_receipt_creates_correct_sle(self):
		doc = self.make_stock_entry("Receipt", qty=10, rate=500, target=self.warehouse_1)
		sles = self.get_sles(doc.name)

		self.assertEqual(len(sles), 1)
		self.assertEqual(sles[0].actual_qty, 10)
		self.assertEqual(sles[0].valuation_rate, 500)
		self.assertEqual(sles[0].stock_value, 5000)
		self.assertEqual(sles[0].warehouse, self.warehouse_1)

	def test_receipt_without_rate_fails(self):
		with self.assertRaises(frappe.ValidationError):
			self.make_stock_entry("Receipt", qty=10, target=self.warehouse_1)

	def test_receipt_without_target_warehouse_fails(self):
		with self.assertRaises(frappe.ValidationError):
			self.make_stock_entry("Receipt", qty=10, rate=500)

	# ---------- Consume ----------

	def test_consume_pulls_current_moving_average_rate(self):
		self.make_stock_entry("Receipt", qty=10, rate=500, target=self.warehouse_1)
		consume = self.make_stock_entry("Consume", qty=4, source=self.warehouse_1)
		sles = self.get_sles(consume.name)

		self.assertEqual(len(sles), 1)
		self.assertEqual(sles[0].actual_qty, -4)
		self.assertEqual(sles[0].valuation_rate, 500)
		self.assertEqual(sles[0].stock_value, -2000)

	def test_consume_without_source_warehouse_fails(self):
		self.make_stock_entry("Receipt", qty=10, rate=500, target=self.warehouse_1)
		with self.assertRaises(frappe.ValidationError):
			self.make_stock_entry("Consume", qty=4)

	def test_consume_with_no_stock_fails(self):
		with self.assertRaises(frappe.ValidationError):
			self.make_stock_entry("Consume", qty=1, source=self.warehouse_1)

	# ---------- Transfer ----------

	def test_transfer_creates_two_sles(self):
		self.make_stock_entry("Receipt", qty=10, rate=500, target=self.warehouse_1)
		transfer = self.make_stock_entry("Transfer", qty=3, source=self.warehouse_1, target=self.warehouse_2)
		sles = self.get_sles(transfer.name)

		self.assertEqual(len(sles), 2)
		out_row = next(s for s in sles if s.warehouse == self.warehouse_1)
		in_row = next(s for s in sles if s.warehouse == self.warehouse_2)

		self.assertEqual(out_row.actual_qty, -3)
		self.assertEqual(in_row.actual_qty, 3)
		self.assertEqual(out_row.valuation_rate, 500)
		self.assertEqual(in_row.valuation_rate, 500)

	def test_transfer_same_source_and_target_fails(self):
		self.make_stock_entry("Receipt", qty=10, rate=500, target=self.warehouse_1)
		with self.assertRaises(frappe.ValidationError):
			self.make_stock_entry("Transfer", qty=3, source=self.warehouse_1, target=self.warehouse_1)

	# ---------- Moving average across multiple receipts ----------

	def test_moving_average_across_multiple_receipts(self):
		# Receipt 1: 10 units @ 500 -> value 5000
		self.make_stock_entry("Receipt", qty=10, rate=500, target=self.warehouse_1)
		# Receipt 2: 10 units @ 700 -> value 7000
		self.make_stock_entry("Receipt", qty=10, rate=700, target=self.warehouse_1)
		# Running: 20 units, value 12000 -> average rate 600

		consume = self.make_stock_entry("Consume", qty=5, source=self.warehouse_1)
		sles = self.get_sles(consume.name)

		self.assertEqual(sles[0].valuation_rate, 600)
		self.assertEqual(sles[0].stock_value, -3000)

	# ---------- Cancel ----------

	def test_cancel_reverses_receipt(self):
		doc = self.make_stock_entry("Receipt", qty=10, rate=500, target=self.warehouse_1)
		doc.cancel()

		sles = frappe.get_all(
			"Stock Ledger Entry",
			filters={"item": self.item_code, "warehouse": self.warehouse_1},
			fields=["actual_qty"],
		)
		total_qty = sum(s.actual_qty for s in sles)
		self.assertEqual(total_qty, 0)

	def test_cancel_reverses_transfer(self):
		self.make_stock_entry("Receipt", qty=10, rate=500, target=self.warehouse_1)
		transfer = self.make_stock_entry("Transfer", qty=3, source=self.warehouse_1, target=self.warehouse_2)
		transfer.cancel()

		wh2_qty = sum(
			s.actual_qty
			for s in frappe.get_all(
				"Stock Ledger Entry",
				filters={"item": self.item_code, "warehouse": self.warehouse_2},
				fields=["actual_qty"],
			)
		)
		self.assertEqual(wh2_qty, 0)
