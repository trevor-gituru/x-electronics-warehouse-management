import frappe
from frappe.utils.nestedset import NestedSet

class Warehouse(NestedSet):
    nsm_parent_field = "parent_warehouse"
