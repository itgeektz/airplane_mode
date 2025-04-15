# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_time, format_duration, get_datetime

class CrewCheckIn(Document):
	pass


@frappe.whitelist()
def update_duration(doc,intime,outtime):
	doc = frappe.get_doc(frappe.parse_json(doc))
	if intime and outtime:
		intime_obj = get_datetime(intime)
		outtime_obj = get_datetime(outtime)
		duration = outtime_obj - intime_obj
		doc.working_hours = duration.total_seconds() / 3600
		doc.save(ignore_permissions=True)
	else:
		doc.working_hours = 0.0
	return {"duration_hours": doc.doc.working_hours}