# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder.functions import Count,Sum

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart()
	labels = [d["airline"] for d in data]
	values = [d["total_amount"] for d in data]
	report_summary = [
		
]
	
	return columns, data, None, chart, report_summary



def get_columns():
	columns = [
		{
			"label": "Airline",
			"fieldname": "airline",
			"fieldtype": "Data",
		},
		{
			"label": "Revenue",
			"fieldname": "total_amount",
			"fieldtype": "Float",
		
		}
	]
	return columns

def get_data(filters=None):
	data = []
	AirplaneTicket = frappe.qb.DocType("Airplane Ticket")
	AirplaneFlight = frappe.qb.DocType("Airplane Flight")
	Airplane = frappe.qb.DocType("Airplane")
	
	total_revenue = Sum(AirplaneTicket.total_amount).as_("total_amount")

	query = ( frappe.qb.from_(AirplaneTicket)
		  .join(AirplaneFlight)
		  .on(AirplaneFlight.name == AirplaneTicket.flight)
		  .join(Airplane)
		  .on(Airplane.name == AirplaneFlight.airplane)
		  .select(
			  Airplane.airline,
			  #AirplaneTicket.total_amount
			  total_revenue
		).groupby(Airplane.airline)
		)

	tickets = query.run(as_dict=True)
	for ticket in tickets:
		row = {
			"airline":ticket.airline,
			"total_amount":ticket.total_amount
		}
		data.append(row)
	

	return data
	
	
def get_chart():
	data = get_data(filters=None)
	labels = [d["airline"] for d in data]
	values = [d["total_amount"] for d in data]
	
	chart = {
    "data": {
        "labels": labels,
        "datasets": [
            {
                "name": "Revenue",
                "values": values
            }
        ]
    },
    "type": "bar"  # Chart type: bar, line, pie, etc.
}
	return chart

