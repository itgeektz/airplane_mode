# Copyright (c) 2024, Nidhi and contributors
# For license information, please see license.txt
from frappe.utils import today,now
import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		if f"{self.date_of_departure} {self.time_of_departure}" > now()  or self.status == 'Scheduled':
			frappe.throw("The flight is still not started the Journey")
		
		tickets = frappe.get_all(
			'Airplane Ticket',
			filters={"flight":self.name,"docstatus":0},
			pluck="name"
		)
		
		if not tickets:
			frappe.msgprint("There is no tickets booked for this flight")
			return
		
		if self.status == 'Completed':
		
			docstatus_value = 1
			ticket_status = 'Boarded'
		
		elif self.status == 'Cancelled':
			docstatus_value = 2
			ticket_status = 'Flight Cancelled'
		
		for ticket in tickets:
			frappe.db.set_value('Airplane Ticket',ticket,'status',ticket_status)
			frappe.db.set_value('Airplane Ticket',ticket,'docstatus',docstatus_value)
		frappe.db.commit()


	
