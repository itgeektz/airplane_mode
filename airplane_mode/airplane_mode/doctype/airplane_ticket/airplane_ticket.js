// Copyright (c) 2024, Nidhi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        if (!frm.doc.seat){
       frm.add_custom_button(__('Seats'), function () {
           check_availablity(frm);
       });
        }
    }
});

function check_availablity(frm) {
    frappe.call({
        method: "airplane_mode.airplane_mode.doctype.airplane_ticket.airplane_ticket.seats_used",
        args: {
            "flight": frm.doc.flight,
            "name": frm.doc.name,
        },
        callback: function (r) {
            if (r.message) {
                let capacity = r.message[0];
                let used_seats = r.message[1].length;
                if (used_seats >= capacity) {
                    frappe.throw(__('Capacity is full'));
                } else {
                    assign_seats(frm);
                }
            }
        }
            
    });
}

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
                dialog.hide(); // Close the dialog after selection
                frm.set_value('seat', selected_seat)
                .then(() => {
                    frm.save();
                    frm.refresh();
                })

            }
        }
    });

    dialog.show(); // Show the dialog
};
