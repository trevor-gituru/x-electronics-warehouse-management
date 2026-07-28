// Copyright (c) 2026, App Publisher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Warehouse', {
  setup(frm) {
    // Restrict parent warehouse options to warehouses marked as groups.
    frm.set_query('parent_warehouse', () => {
      return {
        filters: {
          is_group: 1,
        },
      };
    });
  },
});
