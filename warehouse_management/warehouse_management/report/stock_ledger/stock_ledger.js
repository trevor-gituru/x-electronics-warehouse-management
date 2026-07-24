// Copyright (c) 2026, App Publisher and contributors
// For license information, please see license.txt

frappe.query_reports['Stock Ledger'] = {
  filters: [
    {
      fieldname: 'item',
      label: 'Item',
      fieldtype: 'Link',
      options: 'Item',
    },
    {
      fieldname: 'warehouse',
      label: 'Warehouse',
      fieldtype: 'Link',
      options: 'Warehouse',
    },
    {
      fieldname: 'from_date',
      label: 'From Date',
      fieldtype: 'Date',
    },
    {
      fieldname: 'to_date',
      label: 'To Date',
      fieldtype: 'Date',
    },
  ],
};
