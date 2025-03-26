// Copyright (c) 2024, Nidhi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
 	onload(frm) {
        set_filters(frm);
    
	},
 });

/*
 frm.set_query('Assigned Crew', function () {
    frm.fields_dict["Assigned Crew"].grid.get_field("staff_assigned").get_query = function(doc){
    return {
        filters:{
            "designation": frm.fields_dict["Assigned Crew"].grid.get_field("role")
        }
    }
 }
});
 /*
 frm.set_query("staff_assigned", "assigned_crew", function (doc, cdt, cdn) {
    return {
       filters: {
           // 'designation': frm.doc.assigned_crew_role,
        }
   };
});
 
 frm.set_query('Assigned Crew Staff Assigned', function () {
    return {
        filters: {
            'designation': frm.doc.assigned_crew_role,
            
        }
    };
});

*/