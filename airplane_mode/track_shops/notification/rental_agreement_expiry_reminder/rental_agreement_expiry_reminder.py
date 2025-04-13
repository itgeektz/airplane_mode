import frappe

def get_context(context):
	frappe.db.get_single_value("Rental reminder")
	
