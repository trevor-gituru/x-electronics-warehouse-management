// Copyright (c) 2026, App Publisher and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Ledger"] = {
  // Report filters
  filters: [
    {
      // Filter ledger entries by a specific inventory item
      fieldname: "item",
      label: "Item",
      fieldtype: "Link",
      options: "Item",
    },
    {
      // Filter ledger entries by warehouse
      fieldname: "warehouse",
      label: "Warehouse",
      fieldtype: "Link",
      options: "Warehouse",
    },
    {
      // Show entries posted on or after this date
      fieldname: "from_date",
      label: "From Date",
      fieldtype: "Date",
    },
    {
      // Show entries posted on or before this date
      fieldname: "to_date",
      label: "To Date",
      fieldtype: "Date",
    },
  ],
};
