# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


form_grid_templates = {"items": "templates/form_grid/item_grid.html"}

class RentalInvoice(Document):
	def before_insert(self):
		total_tax = 0
		total_rate = 0
		total_amount = 0
		total_discount = 0
		discounted_amount = 0
		if self.bill:
			total_tax = 0
			total_rate = 0
			total_amount = 0
			total_discount = 0
			discounted_amount = 0
			for item in self.bill:
				item.invoice_qty = 1
				item.rate = 1
				item.total = item.invoice_qty * item.rate
				item.discount = 0
				item.discounted_amount = item.total - item.discount
				item.added_tax = 0
				item.total_amount = item.discounted_amount + item.added_tax
				total_tax += item.added_tax
				total_rate += item.item_rate
				total_qty += item.item_qty
				total_amount += item.total_amount
				total_discount += item.discount
				discounted_amount += item.discounted_amount
			self.total_qty = total_qty
			self.total_amount = total_amount
			self.total_discount = total_discount
			self.total_tax = total_tax
			self.tax_applied_amount = discounted_amount
			frappe.db.commit()
