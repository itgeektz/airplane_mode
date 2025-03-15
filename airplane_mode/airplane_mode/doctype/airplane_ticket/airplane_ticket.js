// Copyright (c) 2024, Nidhi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
 	refresh(frm) {

 	},
     onload: function (frm) {
        
        action(frm);
        
    }
 });

 var action = function (frm) {
    frm.add_custom_button(__('Duplicate'), function () {
        if (click_count > 0) {
            return;
        }
        click_count += 1;

        if (frm.is_dirty()) {
            frm.save();
        }

        frappe.call({
            method: 'airplane_mode.airplane_mode.doctype.airplane_ticket.airplane_ticket.assign_seat',
            args: {
                'flight': frm.doc.flight
            },
            callback: function (data) {
                if (data.message) {
                    frappe.set_route('Form', 'Patient Encounter', data.message);
                    setTimeout(function () {
                        frm.reload_doc();
                    }, 2000);
                }
            }
        });
    

 });
};