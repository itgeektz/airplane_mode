# Copyright (c) 2024, Nidhi and contributors
# For license information, please see license.txt
from frappe.utils import today,now
import frappe
from datetime import timedelta,datetime
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def before_save(self):
		if self.assigned_crew:
			for crew in self.assigned_crew:
				update_crew_timings(self,crew)
				crew_checkin(self,crew)
		departure_gate = frappe.get_doc("Airport Gates",self.departure_gate)
		arrival_gate = frappe.get_doc("Airport Gates",self.arrival_gate)
		if not departure_gate.flight_charted:
			if departure_gate.status == "Available":
				frappe.db.set_value("Airport Gates",self.departure_gate,"flight_charted",self.name)
				frappe.db.set_value("Airport Gates",self.departure_gate,"status","Open")
			else:
				frappe.throw("Please Check the Departure Gate Status")
		elif departure_gate.flight_charted != self.name:
			frappe.throw("The Departure Gate is already booked for another flight")	
		if not arrival_gate.flight_charted:
			if arrival_gate.status == "Available":
				frappe.db.set_value("Airport Gates",self.arrival_gate,"flight_charted",self.name)
				frappe.db.set_value("Airport Gates",self.arrival_gate,"status","Open")
			else:
				frappe.throw("The Arrival Gate is not Available")
		elif arrival_gate.flight_charted != self.name:
			frappe.throw("The Arrival Gate is already booked for another flight")
		frappe.db.commit()
	def on_update(self):
		if self.assigned_crew:
			for crew in self.assigned_crew:
				crew_checkin(self,crew)
				if (crew.assigned_date != self.date_of_departure or 
					crew.assigned_in_time != self.time_of_departure or
					crew.duration_on_air != self.duration):
					update_crew_timings(self,crew)
		airport_gates = frappe.get_all("Airport Gates",
			filters={"flight_charted":self.name},
			fields=["name","flight_charted","status","airport","airport_code"])
		if len(airport_gates) >= 1:
			for gate in airport_gates:
				if gate.name not in [self.departure_gate,self.arrival_gate]:
					frappe.db.set_value("Airport Gates",gate.name,"flight_charted","")
					frappe.db.set_value("Airport Gates",gate.name,"status","Available")
				else:
					frappe.db.set_value("Airport Gates",gate.name,"flight_charted",self.name)
					frappe.db.set_value("Airport Gates",gate.name,"status","Open")
		airport_ticket = frappe.db.get_all("Airplane Ticket",
			filters={"flight":self.name},
			fields = ["name","flight","departure_gate","arrival_gate"]
		)
		for ticket in airport_ticket:
			if self.departure_gate and self.departure_gate != ticket.departure_gate:
				frappe.db.set_value("Airplane Ticket",ticket.name,'departure_gate',self.departure_gate)
				
			if self.arrival_gate and self.arrival_gate != ticket.arrival_gate:
				frappe.db.set_value("Airplane Ticket",ticket.name,'arrival_gate',self.arrival_gate)
				
		frappe.db.commit()
			
	def on_submit(self):
		if f"{self.date_of_departure} {self.time_of_departure}" > now()  or self.status == 'Scheduled':
			frappe.throw("The flight is still not started the Journey")
		
		tickets = frappe.get_all(
			'Airplane Ticket',
			filters={"flight":self.name,"docstatus":0},
			pluck="name"
		)
		
		if tickets:
			if self.status == 'Completed':
				if len(self.airplane_crew) < 1:
					frappe.throw("Please Check the Crew Members")
				docstatus_value = 1
				ticket_status = 'Boarded'
			elif self.status == 'Cancelled':
				docstatus_value = 2
				ticket_status = 'Flight Cancelled'
			for ticket in tickets:
				frappe.db.set_value('Airplane Ticket',ticket,'status',ticket_status)
				frappe.db.set_value('Airplane Ticket',ticket,'docstatus',docstatus_value)
		else:
			frappe.msgprint("There is no tickets booked for this flight")
		self.published = 0
		frappe.db.set_value("Airport Gates",self.arrival_gate,'flight_charted',"")
		frappe.db.set_value("Airport Gates",self.arrival_gate,'status','Available')
		frappe.db.set_value("Airport Gates",self.departure_gate,'flight_charted',"")
		frappe.db.set_value("Airport Gates",self.departure_gate,'status','Available')
		frappe.db.commit()


def update_crew_timings(self,crew):
	"""Update crew timings based on flight details."""
	time_format = "%d-%m-%Y %H:%M:%S"
	tod = datetime.strptime(str(self.time_of_departure), "%H:%M:%S").time()
	dod = datetime.strptime(self.date_of_departure,"%Y-%m-%d").date()
	cdtd = datetime.combine(dod,tod)
	ait = cdtd - timedelta(hours=3)
	duration = timedelta(seconds=self.duration)
	aot = cdtd + duration + timedelta(hours=1)
	crew.assigned_date = self.date_of_departure
	crew.assigned_in_time = ait
	crew.duration_on_air = self.duration
	crew.assigned_end_time = aot
		#crew.save(ignore_permissions=True)
def crew_checkin(self,crew):
	check_in = frappe.get_all("Crew Check In",filters={"check_in_flight":self.name},fields=["crew"])
	crew = frappe.get_all("Assigned Crew",filters={"parent":self.name},fields=["staff_assigned"])
	added = list(set(crew) - set(check_in))
	removed = list(set(check_in) - set(crew))
	if added:
		for a in added:
			crew_check_in = frappe.new_doc("Crew Check In")
			crew_check_in.crew = a
			crew_check_in.flight_assigned = self.name
	if removed:
		for r in removed:
			if frappe.get_value("Crew Check In",filters={"crew":r},fields=['check_in_time']):
				frappe.throw("This is employee is already signed in for this flight. Please shift the attendance or inform the Staff")
			frappe.db.delete("Crew Check In",filters={"crew":r})

	

