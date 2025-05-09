# Copyright (c) 2025, Nidhi and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import date_diff, nowdate,getdate
from airplane_mode.utility import add_comment


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
			return
		for agr in agreements:
			if agr.end_date < today:
				frappe.db.set_value("Rental Agreement",agr.name,'status','Expired')
				frappe.db.set_value("Rental Agreement",agr.name,'rent_reminder',0)
				frappe.db.set_value("Shop", shop.name, "rented", 0)
				update_shop_tally(shop)
				add_comment("Shop", shop.name, "The Agreement Expired on {}".format(agr.end_date), comment_by='Auto Update')
				add_comment("Rental Agreement", agr.name, "The Agreement Expired on {}".format(agr.end_date), comment_by='Auto Update')
				frappe.db.commit()
			else:
				sender = "notifications@example.com"
				recipients = [
				frappe.get_cached_value("Tenant", agr["tenant"], "tenant_email"),
				]
				subject="Rental Reminder for: {0} agreement ending at: {1}".format(shop.name, agr["end_date"])
				header = 'Rental Expiry Reminder'
				if agr.end_date == today:
					message = """Dear Tenant,<br>
								The rental agreement between Airport and you has expired.<br>
								If you have already completed the renewal procedure, it will be updated accordingly.<br>
								In that case, please ignore this email.<br>
								<br>
								It is a pleasure to do business with you.<br><br>
								Regards,<br>
								Airport Management
							"""
					comment_text = "Rental Expiry Reminder sent"
				elif date_diff(getdate(agr["end_date"]), today) < 7:
					message = """Dear Tenant,<br>
								Please consider this as a reminder for the upcoming expiry of the agreement between Airport and you.<br>
								Please take the necessary action.<br><br>
								Regards,<br>
								Airport Management
							"""
					comment_text = "Rental Expiry Reminder before 7 Days sent"
				else:
					add_comment("Scheduled Job Type","shop.check_rental_validity","no action","auto update")
					continue
				frappe.sendmail(
						recipients=recipients,
						sender=sender,
						subject=subject,
						message=message,
						header = header
					)
				add_comment("Shop", shop.name, comment_text, comment_by='Auto Update')
			frappe.db.commit()				

