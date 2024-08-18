// Copyright (c) 2024, Nidhi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airline',{
    refresh: function(frm){
        frm.add_custom_button(__("website"));
    }
}
