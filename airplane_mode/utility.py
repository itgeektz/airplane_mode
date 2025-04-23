import frappe

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