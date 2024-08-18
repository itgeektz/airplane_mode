# Copyright (c) 2024, Nidhi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document

'''
class FlightPassenger(Document):
	def before_save(self):
		frappe.throw("This is me testing")
		#self.full_name = f"{self.first_name} {self.last_name}"
'''

class FlightPassenger(Document):
    def before_save(self):
        if self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        else:
            self.full_name = f"{self.first_name}"