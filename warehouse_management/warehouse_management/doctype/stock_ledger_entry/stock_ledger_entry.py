import frappe
from frappe.model.document import Document


class StockLedgerEntry(Document):
    """Stores immutable records of inventory movements."""

    def autoname(self):
        """Generate a unique name for the stock ledger entry."""
        self.name = frappe.generate_hash(length=10)
