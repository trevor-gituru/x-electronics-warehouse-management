import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet


class Warehouse(NestedSet):
    """Represents a warehouse in a hierarchical inventory structure."""

    nsm_parent_field = "parent_warehouse"

    def validate(self):
        """Validate the warehouse before it is saved."""
        self.validate_parent_is_group()
        self.validate_group_status()

    def validate_parent_is_group(self):
        """Ensure the selected parent warehouse is marked as a group."""
        if not self.parent_warehouse:
            return

        is_group = frappe.db.get_value(
            "Warehouse",
            self.parent_warehouse,
            "is_group",
        )

        if not is_group:
            frappe.throw(
                _(
                    "Parent Warehouse <b>{0}</b> must be marked as a Group warehouse."
                ).format(self.parent_warehouse)
            )

    def validate_group_status(self):
        """Prevent a warehouse with child warehouses from being a non-group."""
        if self.is_group:
            return

        has_children = frappe.db.exists(
            "Warehouse",
            {"parent_warehouse": self.name},
        )

        if has_children:
            frappe.throw(
                _(
                    "Warehouse <b>{0}</b> has child warehouses and must remain marked as a Group."
                ).format(self.name)
            )
