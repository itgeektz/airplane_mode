# Copyright (c) 2024, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Airport(Document):
	def before_save(self):
		if self.airport_gates:
			for gate in self.airport_gates:
				if not gate.airport:
					gate.airport = self.name
					gate.airport_code = self.code
					gate.save(ignore_permissions=True)
			frappe.db.set_value("Airport",self.name,"no_of_gates",len(self.airport_gates))
		else:
			frappe.db.set_value("Airport",self.name,"no_of_gates",0)
		frappe.db.commit()
	def on_update(self):
		if self.airport_gates:
			frappe.db.set_value("Airport",self.name,"no_of_gates",len(self.airport_gates))
		else:
			frappe.db.set_value("Airport",self.name,"no_of_gates",0)
		frappe.db.commit()
