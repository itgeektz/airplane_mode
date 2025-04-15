# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe


def execute(filters):
	frappe.msgprint("This is the filter {0}".format(filters))
	columns = get_columns()
	data = get_data(filters)
	frappe.msgprint("This is columns {0}".format(columns))
	frappe.msgprint("This is data {0}".format(data))
	return columns, data


def get_columns():
	columns = [
		{
			"label": "Crew Id",
			"fieldname": "crew",
			"fieldtype": "Link",
			"options":"Employee"
		},
		{
			"label": "Crew Name",
			"fieldname": "crew_full_name",
			"fieldtype": "Data",
			
		},
		{
			"label": "Assigned Date",
			"fieldname": "assigned_date",
			"fieldtype": "Date",
		},
		{
			"label": "Assigned In Time",
			"fieldname": "assigned_in_time",
			"fieldtype": "time",
		},
		
		{
			"label": "Assigned Out Time",
			"fieldname": "assigned_out_time",
			"fieldtype": "time",
		},
		{
			"label": "Actual Time In",
			"fieldname": "check_in_time",
			"fieldtype": "Datetime",
		},
		{
			"label": "Actual Time Out",
			"fieldname": "check_out_time",
			"fieldtype": "Datetime",
		},
		]
	return columns

def get_data(filters=None):
	if filters:
		data = []
		assigned_crew = frappe.get_all("Assigned Crew",
								 filters={"parent":filters.flight},
								 fields=["*"]
									)
		if not assigned_crew:
			frappe.throw("There is no crew assigned with this flight")
		check_in = frappe.get_all("Crew Check In",
							filters={"check_in_flight":filters.flight},
							fields=['crew',
							'crew_full_name',
							'check_in_time',
							'check_out_time',
							'working_hours'
							]
						)
		if not check_in:
			frappe.throw("There is no crew assigned with Timings,Please redo the crew assignment")
		check_in_map = {item['crew']: item for item in check_in}
		frappe.msgprint("This is each assigned crew {0} and this is each check in \n ".format(assigned_crew))
		for crew in assigned_crew:
			crew_id = crew.staff_assigned
			if crew_id in check_in_map:
				check = check_in_map[crew_id]
				row = {
					"crew": crew_id,
					"crew_full_name": check.get("crew_full_name"),
					"assigned_date": crew.get("assigned_date"),
					"assigned_in_time": crew.get("assigned_in_time"),
					"assigned_out_time": crew.get("assigned_end_time"),
					"check_in_time": check.get("check_in_time"),
					"check_out_time": check.get("check_out_time"),
					"working_hours": check.get("working_hours")
				}
				frappe.msgprint(f"This is the each row {crew_id} - {row}")
				data.append(row)
			
		return data
		
