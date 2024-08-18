# Copyright (c) 2024, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random


class AirplaneTicket(Document):
	
	def before_save(self):
		if self.get("add_ons"):
			item_total_amount = 0
			for item in self.get("add_ons"):
				item_total_amount = item_total_amount + item.amount
			self.total_amount = self.flight_price + item_total_amount
		else:
			self.total_amount = self.flight_price

	def validate(self):
		items = []
		for item in self.get("add_ons"):
			if item.item not in items:
				items.append(item.item)
			else:
				#p = frappe.get_doc("add_ons", item.item)
				#p.remove(item.item)
				frappe.throw("Remove the repeating Item : {} with Price: {} from the Add Ons".format(item.item,item.amount))
	def before_submit(self):		
		if self.status != "Boarded":
			frappe.throw("This is not a valid Status for document submission")
	def before_insert(self):
		airplane = frappe.db.get_value("Airplane Flight",self.flight,"airplane")
		capacity = frappe.db.get_value("Airplane",airplane,"capacity")
		no_of_rows = capacity / 6
		#self.seat = 0
		seat_line = ["A","B","C","D","E"]
		seats_used = frappe.get_all("Airplane Ticket",filters={"flight":self.flight},fields=["seat"],pluck="seat")
		#frappe.msgprint("Seats already booked: {}".format(seats_used))
		self.seat = f"{random.randrange(1,int(no_of_rows))}{random.choice(seat_line)}"
		if self.seat in seats_used:
			self.seat = f"{random.randrange(1,int(no_of_rows))}{random.choice(seat_line)}"

		


	
	
	


			 



