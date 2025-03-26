# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Employee(Document):
	def before_save(self):
		full_name = self.first_name+" "+self.last_name