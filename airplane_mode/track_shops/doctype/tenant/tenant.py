# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Tenant(Document):
	def before_save(self):
		self.tenant_id = self.name
	