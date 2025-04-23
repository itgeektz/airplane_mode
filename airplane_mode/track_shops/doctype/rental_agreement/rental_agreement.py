# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
import datetime
from airplane_mode.utility import add_comment
from airplane_mode.track_shops.doctype.rental_invoice.rental_invoice import accumulate_totals,update_item_defaults

today = nowdate()

class RentalAgreement(Document):
	
	def validate(self):
		validate_one_agreement(self)
		if self.rental_amount <= 0:
			frappe.throw("The rental amount must be set")
		
	def before_submit(self):
		if self.status != "Valid" or self.end_date <= today:
			msg = f"Please check the status set as <b>Valid</b> or Check the <b>Start Date</b> and <b>End Date</b> are in the valid range to submit the document"
			frappe.throw(msg)
	def on_submit(self):
		if self.status == "Valid":
			frappe.db.set_value("Shop",self.shop,'rented',1)
			self.rent_reminder = frappe.db.get_single_value("Rent Reminder",'rent_reminder')

	def before_save(self):
		if self.rental_amount <= 0:
			self.rental_amount = frappe.get_value("Shop",self.shop,'rent_per_month')
	def on_update(self):
		self.rent_reminder = frappe.db.get_single_value("Rent Reminder",'rent_reminder')



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
	
		
def create_monthly_invoice():
	day =  datetime.datetime.strptime(today, "%Y-%m-%d").date()
	if day.day != 16:
		print("Not the 16th – skipping invoice generation.")
		return
	
	if day.day == 16:
		try:
			agreements = frappe.get_all("Rental Agreement",
									filters={
										"status": "Valid",
										"end_date": [">", today],
										"start_date": ["<=", today],
										"payment_intervals": "Monthly"
									},
									fields=[
										"name", "tenant", "shop", "start_date", "end_date",
										"price_list", "shop_rate", "shop_size", "airport",
										"airport_code", "tenant_email"
									])
		except Exception as e:
			frappe.log_error(message=str(e), title="Error fetching agreements")
			print("Error fetching agreements:", e)
			return
		
		totals = {"total_tax" : 0,
		"total_rate" : 0,
		"total_qty" : 0,
		"total_amount" : 0,
		"total_discount" : 0,
		"discounted_amount" : 0 }
		
		for agreement in agreements:
			invoice = frappe.db.exists("Rental Invoice",
							 {
								 "rental_agreement":agreement.name,
								 "invoice_date":datetime.datetime.strptime(today, "%Y-%m-%d").date()
								 })
			if invoice:
				frappe.log_error(message="invoice_not_generated", title=f"Invoice is already exists for {agreement['name']}")
				continue
			try:
				inv = frappe.get_doc({
					"doctype":"Rental Invoice",
					"rental_agreement": agreement.name,
					"shop":agreement.shop,
					"tenant":agreement.tenant,
					"airport":agreement.airport,
					"invoice_date": datetime.datetime.strptime(today, "%Y-%m-%d").date(),
					"due_date": datetime.datetime.strptime(today, "%Y-%m-%d").date() + datetime.timedelta(days=7),
					"price_list":agreement.price_list,
					"tenant_email":agreement.tenant_email,
				})
				# prepare item
				item = frappe._dict({
					"invoice_item": "Shop Rent",
					"invoice_qty": agreement.shop_size,
					"rate": agreement.shop_rate,
					"total": agreement.shop_size * agreement.shop_rate,
					"price_list": agreement.price_list,
					"agreement_reference": agreement.name,
					"agreement_start_date": agreement.start_date,
					"agreement_end_date": agreement.end_date,
					"discount": 0,
					"tax": frappe.db.get_single_value('Tax', 'tax_percentage')
				})

				# use external functions
				update_item_defaults(item)
				accumulate_totals(item, totals)
				item_list = [item]
				# add to child table
				for processed_item in item_list:
					inv.append("bill", processed_item)

				inv.save(ignore_permissions=True)
				frappe.db.commit()
				inv.submit()
				add_comment("Rental Agreement",inv.name,"Agreement generated","auto update")
				add_comment("Shop",inv.shop,"Agreement generated","auto update")
				
			except Exception as inv_error:
				frappe.log_error(message=str(inv_error), title=f"Invoice creation failed for {agreement['name']}")
				print(f"Failed to create invoice for agreement {agreement['name']}:", inv_error)

