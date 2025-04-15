# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder.functions import Sum,Date

def execute(filters=None):
	columns = get_columns()
	airline = filters.airline
	end_date = filters.get("end_date")

	data = get_data(airline)
	chart = get_chart(data)
	labels = [d["airline"] for d in data]
	values = [d["total_amount"] for d in data]
	report_summary = get_summary(data)
	
	return columns, data, None, chart, report_summary



def get_columns():
	columns = [
		{
			"label": "Airline",
			"fieldname": "airline",
			"fieldtype": "Link",
			"options":"Airline"
		},
		{
			"label": "Revenue",
			"fieldname": "total_amount",
			"fieldtype": "Currency",
		
		},
		
	]
	return columns


def get_data(airline):
    AirplaneTicket = frappe.qb.DocType("Airplane Ticket") 
    AirplaneFlight = frappe.qb.DocType("Airplane Flight")
    Airplane = frappe.qb.DocType("Airplane")

    # Extract only the date part from the timestamp
    date_only = Date(AirplaneTicket.creation).as_("date")

    total_revenue = Sum(AirplaneTicket.total_amount).as_("total_amount")

    query = (
        frappe.qb.from_(AirplaneTicket)
        .join(AirplaneFlight).on(AirplaneFlight.name == AirplaneTicket.flight)
        .join(Airplane).on(Airplane.name == AirplaneFlight.airplane)
        .select(
            #date_only,  # Group by date only, ignoring time
            Airplane.airline,
            total_revenue  # Summing the total_amount
        )
		.where(Airplane.airline == airline)#(date_only >= start_date) & (date_only <= end_date))
    	.groupby(Airplane.airline)
    )

    tickets = query.run(as_dict=True)
    frappe.msgprint("This is tickets {0}".format(tickets))
    return tickets

	
def get_chart(data):
	labels = [d["airline"] for d in data]
	values = [d["total_amount"] for d in data]
	
	chart = {
    "data": {
        "labels": labels,
        "datasets": [
            {
                "name": "Revenue",
                "values": values,
				"fieldtype": "Currency",
            }
        ]
    },
    "type": "pie"  # Chart type: bar, line, pie, etc.
}
	return chart

def get_summary(data):
	report_summary = []
	for d in data:
		row = {
			"label": d.airline,
			"value":d.total_amount
		}
		report_summary.append(row)
	return report_summary