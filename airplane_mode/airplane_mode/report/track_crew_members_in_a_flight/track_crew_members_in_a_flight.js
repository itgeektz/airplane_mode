// Copyright (c) 2025, Nidhi and contributors
// For license information, please see license.txt

frappe.query_reports["track crew members in a flight"] = {
	"filters": [{
		fieldname: "flight",
		label: "Flight",
		fieldtype: "Link",
		options: "Airplane Flight",
		on_change: function(query_report){
			query_report.refresh();
		}
		
	},
	]
};
