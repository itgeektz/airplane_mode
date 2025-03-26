import frappe
from airplane_mode.airplane_mode.doctype.airplane_ticket.airplane_ticket import assign_seats

def execute():
    list = frappe.db.get_list("Employee",fields=["name","first_name","middle_name","last_name","full_name"])
    for l in list:
        full_name = l.first_name+" "+l.last_name
        frappe.db.set_value("Employee",l.name,'full_name',full_name)