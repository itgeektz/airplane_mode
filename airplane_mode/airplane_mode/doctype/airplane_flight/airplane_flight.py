# Copyright (c) 2024, Nidhi and contributors
# For license information, please see license.txt
from frappe import utils
import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		if self.date_of_departure > utils.today() and self.time_of_departure > utils.now():
			frappe.throw("The flight is still not started the Journey")
		self.status = 'Completed'
		if self.status != 'Completed':
			frappe.throw("Status should be completed before submit")
	
