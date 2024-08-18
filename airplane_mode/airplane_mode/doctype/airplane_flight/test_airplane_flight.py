# Copyright (c) 2024, Nidhi and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestAirplaneFlight(FrappeTestCase):
	def before_submit(self):
		self.status = 'Completed'
		if self.status != 'Completed':
			frappe.throw("Status should be completed before submit")
			
