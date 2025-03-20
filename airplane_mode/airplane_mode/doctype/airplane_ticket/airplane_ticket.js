// Copyright (c) 2024, Nidhi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        if (!frm.doc.seat){
       frm.add_custom_button(__('Seats'), function () {
           assign_seats(frm);
       }, __('Seats'));
        }
    }
});



var assign_seats = function (frm) {
    var dialog = new frappe.ui.Dialog({
        title: 'Select a Seat',
        fields: [
            {
                fieldtype: 'Data', 
                label: "Seat", 
                reqd: 1, 
                fieldname: 'seat'
            }
        ],
        primary_action_label: __('Assign Seat'),
        primary_action: function () {
            let selected_seat = dialog.get_value('seat');
            if (selected_seat) {
                frappe.model.set_value(frm.doctype, frm.docname, 'seat', selected_seat);
                dialog.hide(); // Close the dialog after selection
            }
        }
    });

    dialog.show(); // Show the dialog
};

/*
 let assign_seats = function (frm) {
	frappe.call({
		method: "airplane_mode.airplane_mode.doctype.airplane_ticket.airplane_ticket.assign_seats",
		args: { flight: frm.doc.flight },  // Corrected from doc.flight
		callback: function (data) {
			if (data.message && data.message.seat) {
				frappe.model.set_value(frm.doctype, frm.docname, 'seat', data.message.seat);
			} else {
				frappe.msgprint(__('No available seats.'));
			}
		}
	});
};
*/