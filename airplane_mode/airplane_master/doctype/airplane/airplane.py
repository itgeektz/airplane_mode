# Copyright (c) 2024, Nidhi and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

'''
class Airplane(Document):
	def before_save(self):
		self.add = f"{self.headquarters}"
		#frappe.throw("This is me testing")
'''

class Airplane(Document):
    def before_save(self):
        self.add = f"{self.headquarters}"
        
