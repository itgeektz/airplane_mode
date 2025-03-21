// Copyright (c) 2025, Nidhi and contributors
// For license information, please see license.txt

frappe.query_reports["Revenue by Airline"] = {
	"filters": [{
    fieldname: "airline",
    label: "Airline",
    fieldtype: "Link",
	options: "Airline",
	on_change: function(query_report){
		query_report.refresh();
	}
    
},
]

};
