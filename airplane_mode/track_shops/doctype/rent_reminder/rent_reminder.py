# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentReminder(Document):
	def on_update(self):
		agreements = frappe.db.get_all("Rent Agreement",pluck='name')
		for agreement in agreements:
			frappe.db.set_value("Rent Agreement",agreement,'rent_reminder',self.rent_reminder)
			frappe.db.commit()
