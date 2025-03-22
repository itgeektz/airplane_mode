# Copyright (c) 2024, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
import string


class AirplaneTicket(Document):
	
	def before_save(self):
		if self.get("add_ons"):
			total_amount = 0
			for item in self.get("add_ons"):
				total_amount = total_amount + item.amount
			self.total_amount = self.flight_price + total_amount
		else:
			self.total_amount = self.flight_price
		
	def validate(self):
		capacity, used_seats = seats_used(self.flight,self.name)
		if capacity <= len(used_seats):
				frappe.throw("capacity is full")
		seen_items = set()
		for item in self.get("add_ons", []):
			if item.item in seen_items:
				raise frappe.throw("Remove the repeating Item : {} with Price: {} from the Add Ons".format(item.item,item.amount))
			seen_items.add(item.item)
		if self.seat:
			if self.seat in used_seats:
				frappe.throw("This seat is already used")
		
	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("This is not a valid Status for document submission")
		if not self.seat:
			seat_data = assign_seats(self.flight,self.name)
			if seat_data and seat_data.get("seat"):
				self.seat = seat_data["seat"]
			else:
				frappe.throw("No seats available for assignment")

def assign_seats(flight,name):
	capacity,used_seats = seats_used(flight,name)
	if capacity <= len(used_seats):
		frappe.throw("capacity is full")
	no_of_columns = 9
	A_Z = list(string.ascii_uppercase)
	if capacity < no_of_columns:
		no_of_rows = 2
		seat_line = A_Z[:capacity]
	else:
		no_of_rows = capacity / no_of_columns
		seat_line = A_Z[:no_of_columns]
	seat = f"{random.randrange(1,int(no_of_rows))}{random.choice(seat_line)}"
	if seat in used_seats:
		seat = f"{random.randrange(1,int(no_of_rows))}{random.choice(seat_line)}"
	return {"seat": seat}

@frappe.whitelist()
def seats_used(flight,name):
	airplane = frappe.db.get_value("Airplane Flight",flight,"airplane")
	seats_used = frappe.get_all("Airplane Ticket",filters={"flight":flight,"name":["!=", name]},fields=["seat"],pluck="seat")
	capacity = frappe.db.get_value("Airplane",airplane,"capacity")
	return capacity,seats_used




	
	
	


			 



