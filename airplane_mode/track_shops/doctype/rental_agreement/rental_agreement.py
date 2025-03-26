# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

today = nowdate()

class RentalAgreement(Document):
	
	def validate(self):
		validate_one_agreement(self)
		if self.rental_amount <= 0:
			frappe.throw("The rental amount must be set")
		
	def before_submit(self):
		if self.status != "Valid" or self.start_date >= today or self.end_date <= today:
			msg = f"Please check the status set as <b>Valid</b> or Check the <b>Start Date</b> and <b>End Date</b> are in the valid range to submit the document"
			frappe.throw(msg)
	def on_submit(self):
		if self.status == "Valid":
			frappe.db.set_value("Shop",self.shop,'rented',1)

	def before_save(self):
		if self.rental_amount <= 0:
			rent_per_month = frappe.get_value("Shop",self.shop,'rent_per_month')
			frappe.db.set_value("Rental Agreement",self.name,'rental_amount',rent_per_month)



def validate_one_agreement(self):
	agreement = frappe.db.get_list("Rental Agreement",
								filters={"shop":self.shop,
									"status":["in",["Valid"]],
									"docstatus":1
									},
									pluck='name'
									)
	if agreement:
		frappe.throw("Already one agreement is in place for this shop. Either wait for End of Contract or Termination")
	
		
		

