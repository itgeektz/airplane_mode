import frappe
from airplane_mode.airplane_mode.doctype.airplane_ticket.airplane_ticket import assign_seats

def execute():
	print("Started the patch")
	frappe.msgpint("Started the patch")
	list_of_tickets = frappe.db.get_list("Airplane Ticket",fields=["name","seat","flight"])
	for ticket in list_of_tickets:
		if not ticket.seat:
			print("patching",seat_data)
			seat_data = assign_seats(ticket.flight)
			if seat_data and seat_data.get("seat"):
				seat = seat_data["seat"]
				ticket.seat = seat
				frappe.db.commit()
			else:
				print("Failed the patch")
				frappe.throw("No seats available for assignment")
        

 
 