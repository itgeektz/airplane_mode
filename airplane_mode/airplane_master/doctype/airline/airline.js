// Copyright (c) 2025, Nidhi and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Airline", {
    refresh(frm) {
        const stream_link = frm.doc.stream_link;
        frm.add_web_link(stream_link, "View in YouTube");
     },
 });
