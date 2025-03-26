# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, nowdate,getdate


class Shop(Document):
	def before_save(self):
		self.size = self.width * self.length
		self.rent_per_month = self.size * self.rate_per_sqm

	
	
def check_rental_validity():
	today = getdate(nowdate())
	shops = frappe.db.get_all("Shop",filters={"rented":1},fields=['name','rented'])
	for shop in shops:
		agreements = frappe.db.get_list("Rental Agreement",
									filters={"shop":shop.name,
										"docstatus":1,
										"start_date":["<=",today],
										"status":["in",["Valid","Open"]]
										},
										fields=['name','status','start_date','end_date','tenant']
										)
		if not agreements:
			frappe.db.set_value("Shop", shop.name, "rented", 0)
		else:
			for agr in agreements:
				if agr.end_date <= today:
					frappe.db.set_value("Rental Agreement", agr.name, "status", "Expired")
					frappe.db.set_value("Shop", shop.name, "rented", 0)
				elif date_diff(getdate(agr["end_date"]), today) < 7:
					sender = "notifications@example.com"
					recipients = [
				    frappe.get_cached_value("Tenant", agr["tenant"], "tenant_email"),
    				'nidhin.regency@gmail.com'
					]
					message = "Dear Tenant, \n " \
					"Please consider this as reminder for upcoming expiry of the agreement between Airport and you." \
					" Please take the necessary action" \
					"Regards" \
					"" \
					"Airport Management"
					frappe.sendmail(
					recipients=recipients,
					sender=sender,
					subject=frappe._("Rental Reminder for: {} agreement ending at: {}".format(shop.name, agr["end_date"])),
					template='Rental Reminder',
					args=dict(
						#birthday_persons=birthday_persons,
						message=message,
					),
					header = 'Rental Expiry Reminder'
				)
	frappe.db.commit()
				
	
