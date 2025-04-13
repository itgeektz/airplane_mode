// Copyright (c) 2024, Nidhi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Gates", {
    refresh(frm) {
        frm.set_query("terminal", function() {
            return {
                filters: {
                    "docstatus": 1
                }
            };
        });
    },

 });

