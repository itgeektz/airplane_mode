// Copyright (c) 2025, Nidhi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Crew Check In", {
    check_out_time: function(frm,cdt,cdn){
        let row = locals[cdt][cdn];
        if(check_out_time){
            frappe.call({
                method:"airplane_mode.doctype.crew_check_in.crew_check_in.update_duration",
                args: {
                    doc: frm.doc, // or child row
                    intime: row.check_in_time,
                    outtime: row.check_out_time
                },
                callback: (r) => {
                    if (r.messae) {
                        frappe.msgprint(`Duration: ${r.message.duration_hours} hours`);
                    }
                }
            });
        }
    }
 });
