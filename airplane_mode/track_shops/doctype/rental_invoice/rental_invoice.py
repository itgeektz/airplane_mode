# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


form_grid_templates = {"items": "templates/form_grid/item_grid.html"}

class RentalInvoice(Document):
	def validate(self):
		update_bill(self)
		
	def before_submit(self):
		for item in self.bill:
			if not item.discount_approved_by and not item.discounting_notes:
				frappe.throw("The item {0} pending for discount approval.".format(item.invoice_item))
			
				
def update_bill(self):
	totals = {"total_tax" : 0,
		"total_rate" : 0,
		"total_qty" : 0,
		"total_amount" : 0,
		"total_discount" : 0,
		"discounted_amount" : 0 }
	if self.bill:
		for item in self.bill:
			if item.invoice_item == "Shop Rent":
				item.invoice_qty = frappe.get_cached_value("Shop",self.shop,'size')
				item.rate = frappe.get_cached_value("Shop",self.shop,'rate_per_sqm')
				item.total = item.rate * item.invoice_qty
			else:
				item.rate = frappe.get_value("Item Price",
									filters={"item":item.invoice_item,"price_list":self.price_list},
									fieldname="item_rate")
				if not item.rate:
					frappe.throw("Please set the price for rental particular at item price")
				if item.invoice_qty < 1:
					frappe.throw("Please set the qty for item {0}".format(item.invoice_item))
				item.total = item.rate * item.invoice_qty
			item.price_list = self.price_list
			item.agreement_reference = self.rental_agreement
			item.agreement_start_date = frappe.get_cached_value("Rental Agreement",self.rental_agreement,'start_date') 
			item.agreement_start_date = frappe.get_cached_value("Rental Agreement",self.rental_agreement,'end_date') 
			update_item_defaults(item)
			accumulate_totals(item, totals)

			self.total_qty = totals["total_qty"]
			self.total_amount = totals["total_amount"]
			self.total_discount = totals["total_discount"]
			self.total_tax = totals["total_tax"]
			self.tax_applied_amount = totals["discounted_amount"] + totals["total_tax"]
			self.amount_after_discount = self.total_amount - self.total_discount

def update_item_defaults(item):
	if item.discount:
		if item.discount_type == 'Percentage':
			item.discounted_amount = item.total - (item.total * item.discount / 100)
		elif not item.discount_type or item.discount_type == 'In Amount':
			item.discounted_amount = item.total - item.discount
	else:
		item.discounted_amount = item.total
	item.added_tax = (item.discounted_amount * item.tax)/100 if item.tax else 0
	item.total_amount = item.discounted_amount + (item.added_tax if item.added_tax else 0)
	item.inclusive_tax = item.discounted_amount + (item.added_tax if item.added_tax else 0)
	
	

def accumulate_totals(item, totals):
	totals["total_tax"] += item.added_tax or 0
	totals["total_rate"] += item.rate
	totals["total_qty"] += item.invoice_qty
	totals["total_amount"] += item.total
	totals["total_discount"] += item.discount or 0
	totals["discounted_amount"] += item.discounted_amount or 0
