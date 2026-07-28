// Copyright (c) 2026, App Publisher and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Balance"] = {
  // Report filters
  filters: [
    {
      // Show stock balances as of the selected date
      fieldname: "as_on_date",
      label: "As On Date",
      fieldtype: "Date",
      default: frappe.datetime.get_today(),
    },
    {
      // Optionally filter results by a specific item
      fieldname: "item",
      label: "Item",
      fieldtype: "Link",
      options: "Item",
    },
    {
      // Optionally filter results by a specific warehouse
      fieldname: "warehouse",
      label: "Warehouse",
      fieldtype: "Link",
      options: "Warehouse",
    },
  ],
};
