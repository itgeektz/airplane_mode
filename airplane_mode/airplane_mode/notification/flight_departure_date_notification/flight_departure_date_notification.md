<h3>Departs in 24 hours!</h3>

<p>The Flight {{ doc.name }} is due to departure with in 24 Hours from now. Please Keep travel ready.</p>

<p><!-- show last comment -->
{% if comments %}
Last comment: {{ comments[-1].comment }} by {{ comments[-1].by }}
{% endif %}</p>

<h4>Details</h4>

<ul>
<li>Flight: {{ doc.airplane }}
<li>From: {{ doc.source_airport_code }} To : {{ destination_airport_code }}
<li>Departure Date & Time: {{ doc.date_of_departure }} || {{ doc.date_of_time }}
<li>Duration: {{ frappe.utils.format_duration(doc.duration) }}
</ul>
