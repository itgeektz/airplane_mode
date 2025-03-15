import frappe

def execute():
    list_of_tickets = frappe.get_all("Airplane Ticket",filters={"seat":None},field=["name","seat","flight"])
    for ticket in list_of_tickets:
        airplane = frappe.db.get_value("Airplane Flight",ticket.flight,"airplane")
        capacity = frappe.db.get_value("Airplane",airplane,"capacity")
        no_of_rows = capacity / 6
        #ticket.seat = 0
        seat_line = ["A","B","C","D","E"]
        seats_used = frappe.get_all("Airplane Ticket",filters={"flight":ticket.flight},fields=["seat"],pluck="seat")
        #frappe.msgprint("Seats already booked: {}".format(seats_used))
        ticket.seat = f"{random.randrange(1,int(no_of_rows))}{random.choice(seat_line)}"
        if ticket.seat in seats_used:
            ticket.seat = f"{random.randrange(1,int(no_of_rows))}{random.choice(seat_line)}"

 
 