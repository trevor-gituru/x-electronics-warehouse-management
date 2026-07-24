// Copyright (c) 2026, App Publisher and contributors
// For license information, please see license.txt

frappe.query_reports['Stock Balance'] = {
  filters: [
    {
      fieldname: 'as_on_date',
      label: 'As On Date',
      fieldtype: 'Date',
      default: frappe.datetime.get_today(),
    },
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
  ],
};
