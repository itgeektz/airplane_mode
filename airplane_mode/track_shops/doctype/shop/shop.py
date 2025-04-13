# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import date_diff, nowdate,getdate


class Shop(WebsiteGenerator):
	def before_save(self):
		self.size = self.width * self.length
		self.rent_per_month = self.size * self.rate_per_sqm
	
	
		
def update_shop_tally(self,method=None):
	if not self.airport:
		frappe.throw("No Airport linked to this Shop!")
	
	shops = frappe.get_all("Shop", filters={"airport": self.airport}, fields=["name", "rented"])
	
	total_shops = len(shops)
	rented_shops = sum(1 for shop in shops if shop.rented == 1)
	available_shops = total_shops - rented_shops
	frappe.db.set_value("Airport", self.airport, "no_of_shops", total_shops)
	frappe.db.set_value("Airport", self.airport, "shops_rented", rented_shops)
	frappe.db.set_value("Airport", self.airport, "shops_available", available_shops)
	frappe.db.commit()
	


def check_rental_validity():
	today = getdate(nowdate())
	shops = frappe.db.get_all("Shop",filters={"rented":1},pluck='name')
	for shop in shops:
		shop = frappe.get_doc("Shop",shop)
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
			update_shop_tally(shop)
			frappe.db.comit()
		else:
			for agr in agreements:
				sender = "notifications@example.com"
				recipients = [
				frappe.get_cached_value("Tenant", agr["tenant"], "tenant_email"),
				'nidhin.regency@gmail.com'
				]
				subject="Rental Reminder for: {0} agreement ending at: {1}".format(shop.name, agr["end_date"])
				header = 'Rental Expiry Reminder'
				if agr.end_date == today:
					frappe.db.set_value("Rental Agreement", agr.name, "status", "Expired")
					frappe.db.set_value("Shop", shop.name, "rented", 0)
					update_shop_tally(shop)
					message = "Dear Tenant, \n " \
					"The Rental agreement between Airport and you has been Expired." \
					"If you are already done the procedure to renew it will be updated so." \
					"In that case please ignore the email" \
					"It is pleasure to do Business with you" \
					"Regards" \
					"" \
					"Airport Management"
					frappe.sendmail(
						recipients=recipients,
						sender=sender,
						subject=subject,
						args=dict(
							message=message,
						),
						header = header
					)
					add_comment("Shop", shop.name, "Rental Expiry Reminder sent", comment_by='Auto Update')
				elif date_diff(getdate(agr["end_date"]), today) < 7:
					message = "Dear Tenant, \n " \
					"Please consider this as reminder for upcoming expiry of the agreement between Airport and you." \
					" Please take the necessary action" \
					"Regards" \
					"" \
					"Airport Management"
					frappe.sendmail(
					recipients=recipients,
					sender=sender,
					subject=subject,
					args=dict(
						message=message,
					),
					header = header
				)
				add_comment("Shop", shop.name, "Rental Expiry Reminder before 7 Days sent", comment_by='Auto Update')
			frappe.db.commit()				
	
def add_comment(reference_doctype, reference_name, comment_text, comment_by=None):
    comment = frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Comment",
        "reference_doctype": reference_doctype,
        "reference_name": reference_name,
        "content": comment_text,
        "comment_by": comment_by or frappe.session.user  # Defaults to current user
    })
    comment.insert(ignore_permissions=True)
    frappe.db.commit()  # Ensure it's saved to the database
    return comment.name