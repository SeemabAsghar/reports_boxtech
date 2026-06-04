# Copyright (c) 2026, seemabasghar04@gmail.com
# For license information, please see license.txt

import frappe
from frappe import _
from collections import defaultdict


def execute(filters=None):

    filters = frappe._dict(filters or {})

    user = frappe.session.user

    # Roles with full access
    manager_roles = [
        "System Manager",
        "Sales Master Manager",
        "Sales Manager"
    ]

    has_full_access = any(
        role in frappe.get_roles(user)
        for role in manager_roles
    )

    # Sales Users can only see their own data
    if not has_full_access:
        filters.sales_person = user

    columns = get_columns(filters)

    activities = get_all_activities(filters)
    data = apply_grouping(filters, activities)

    report_summary = get_report_summary(activities)

    chart = get_chart_data(activities)

    return columns, data, None, chart, report_summary
# =========================================================
# COLUMNS
# =========================================================
def get_columns(filters):

    group_by = (filters.get("group_by") or "").strip()

    if group_by == "Sales Person":
        return get_sales_person_columns()

    elif group_by == "Activity Type":
        return get_activity_type_columns()

    elif group_by == "Client":
        return get_client_columns()

    return get_detailed_columns()

def get_sales_person_columns():

    return [
        {
            "label": _("Sales Person"),
            "fieldname": "sales_person",
            "fieldtype": "Data",
            "width": 220
        },
        {
            "label": _("Total Activities"),
            "fieldname": "total_activities",
            "fieldtype": "Int",
            "width": 140
        },
        {
            "label": _("Phone Calls"),
            "fieldname": "phone_calls",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": _("Emails"),
            "fieldname": "emails",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Meetings"),
            "fieldname": "meetings",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Quotations"),
            "fieldname": "quotations",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Tasks"),
            "fieldname": "tasks",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Unique Clients"),
            "fieldname": "unique_clients",
            "fieldtype": "Int",
            "width": 140
        }
    ]


def get_activity_type_columns():

    return [
        {
            "label": _("Activity Type"),
            "fieldname": "activity_type",
            "fieldtype": "Data",
            "width": 220
        },
        {
            "label": _("Total Count"),
            "fieldname": "total_count",
            "fieldtype": "Int",
            "width": 140
        },
        {
            "label": _("Unique Clients"),
            "fieldname": "unique_clients",
            "fieldtype": "Int",
            "width": 140
        },
        {
            "label": _("Sales Persons Involved"),
            "fieldname": "sales_persons_involved",
            "fieldtype": "Int",
            "width": 180
        }
    ]


def get_client_columns():

    return [
        {
            "label": _("Client"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 220
        },
        {
            "label": _("Total Activities"),
            "fieldname": "total_activities",
            "fieldtype": "Int",
            "width": 140
        },
        {
            "label": _("Phone Calls"),
            "fieldname": "phone_calls",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": _("Emails"),
            "fieldname": "emails",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Meetings"),
            "fieldname": "meetings",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Quotations"),
            "fieldname": "quotations",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Tasks"),
            "fieldname": "tasks",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Last Activity Date"),
            "fieldname": "last_activity_date",
            "fieldtype": "Date",
            "width": 150
        }
    ]

def get_detailed_columns():

    return [

        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("Time"),
            "fieldname": "time",
            "fieldtype": "Time",
            "width": 90
        },
        {
            "label": _("Sales Person"),
            "fieldname": "sales_person",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Activity Type"),
            "fieldname": "activity_type",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Lead / Opportunity"),
            "fieldname": "lead_opportunity",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Subject"),
            "fieldname": "subject",
            "fieldtype": "Data",
            "width": 220
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Reference"),
            "fieldname": "reference",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Created By"),
            "fieldname": "created_by",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Description"),
            "fieldname": "description",
            "fieldtype": "Small Text",
            "width": 300
        }
    ]


# =========================================================
# GET ALL ACTIVITIES
# =========================================================

def get_all_activities(filters):

    activities = []
    activities.extend(get_customer_activities(filters))
    activities.extend(get_communications(filters))
    activities.extend(get_tasks(filters))
    activities.extend(get_quotations(filters))

    return activities

# =========================================================
# CUSTOMER ACTIVITIES
# =========================================================

def get_customer_activities(filters):

    conditions = ""

    if filters.get("sales_person"):
        conditions += " AND cad.owner = %(sales_person)s "

    if filters.get("customer"):
        conditions += " AND cad.parent = %(customer)s "

    data = frappe.db.sql(f"""
        SELECT
            cad.date,
            cad.time,
            cad.owner as sales_person,
            cad.activity_type,
            cad.result,
            cad.progress,
            cad.phone_call_scenario,
            cad.parent as customer,
            cust.customer_name
        FROM `tabCustomer Activity Detail` cad
        LEFT JOIN `tabCustomer` cust
            ON cust.name = cad.parent
        WHERE cad.date BETWEEN %(from_date)s AND %(to_date)s
        {conditions}
    """, filters, as_dict=True)

    activities = []

    for row in data:

        activity_type = normalize_activity_type(row.activity_type)

        # Activity Type Filter
        if filters.get("activity_type") \
            and filters.get("activity_type") != "All Activities":

            if activity_type != filters.get("activity_type"):
                continue

        # Status Filter
        if filters.get("status"):

            status_map = {
                "Completed": "✅Complete",
                "Pending": "⏳In Progress"
            }

            selected_status = status_map.get(
                filters.get("status"),
                filters.get("status")
            )

            if row.progress != selected_status:
                continue

        activities.append({
            "date": row.date,
            "time": row.time,
            "sales_person": row.sales_person,
            "activity_type": activity_type,
            "customer": row.customer,
            "lead_opportunity": "",
            "subject": row.phone_call_scenario or activity_type,
            "description": row.result,
            "status": row.progress,
            "reference": row.customer,
            "reference_doctype": "Customer",
            "created_by": row.sales_person
        })

    return activities

# =========================================================
# COMMUNICATIONS
# =========================================================

def get_communications(filters):

    conditions = get_conditions(filters, "owner")

    data = frappe.db.sql(f"""
        SELECT
            DATE(creation) as date,
            TIME(creation) as time,
            owner as sales_person,
            subject,
            content,
            communication_type,
            reference_doctype,
            reference_name,
            creation,
            sender,
            status
        FROM `tabCommunication`
        WHERE creation BETWEEN %(from_date)s AND %(to_date)s
        {conditions}
    """, filters, as_dict=True)

    activities = []

    for row in data:

        activity_type = classify_communication(row)

        # Activity Type Filter
        if filters.get("activity_type") \
            and filters.get("activity_type") != "All Activities":

            if activity_type != filters.get("activity_type"):
                continue

        # Status Filter
        if filters.get("status"):

            if row.status != filters.get("status"):
                continue
        # # Customer Filter
        # if filters.get("customer") and row.get("customer") != filters.get("customer"):
        #     continue

        activities.append({
            "date": row.date,
            "time": row.time,
            "sales_person": row.sales_person,
            "activity_type": activity_type,
            "customer": "",
            "lead_opportunity": row.reference_name,
            "subject": row.subject,
            "status": row.status,
            "reference": row.reference_name,
            "reference_doctype": row.reference_doctype,
            "created_by": row.sender
        })

    return activities
# =========================================================
# TASKS
# =========================================================

def get_tasks(filters):

    conditions = get_conditions(filters, "owner")

    data = frappe.db.sql(f"""
        SELECT
            DATE(creation) as date,
            TIME(creation) as time,
            owner as sales_person,
            subject,
            status,
            name,
            creation
        FROM `tabTask`
        WHERE creation BETWEEN %(from_date)s AND %(to_date)s
        {conditions}
    """, filters, as_dict=True)

    activities = []

    for row in data:

        # Activity Type Filter
        if filters.get("activity_type") \
            and filters.get("activity_type") not in ["All Activities", "Task"]:
            continue

        # Status Filter
        if filters.get("status"):

            if row.status != filters.get("status"):
                continue
        # Customer Filter
        # if filters.get("customer"):
        #     continue

        activities.append({
            "date": row.date,
            "time": row.time,
            "sales_person": row.sales_person,
            "activity_type": "Task",
            "customer": "",
            "lead_opportunity": "",
            "subject": row.subject,
            "status": row.status,
            "reference": row.name,
            "reference_doctype": "Task",
            "created_by": row.sales_person
        })

    return activities

# =========================================================
# QUOTATIONS
# =========================================================

def get_quotations(filters):

    conditions = get_conditions(filters, "owner")

    data = frappe.db.sql(f"""
        SELECT
            transaction_date as date,
            owner as sales_person,
            customer_name as customer,
            opportunity,
            name,
            status,
            grand_total
        FROM `tabQuotation`
        WHERE transaction_date BETWEEN %(from_date)s AND %(to_date)s
        {conditions}
    """, filters, as_dict=True)

    activities = []

    for row in data:

        # Activity Type Filter
        if filters.get("activity_type") \
            and filters.get("activity_type") not in ["All Activities", "Quotation"]:
            continue

        # Customer Filter
        if filters.get("customer"):

            if row.customer != filters.get("customer"):
                continue

        # Status Filter
        if filters.get("status"):

            if (row.status or "").lower() != (filters.get("status") or "").lower():
                continue

        activities.append({
            "date": row.date,
            "time": "",
            "sales_person": row.sales_person,
            "activity_type": "Quotation",
            "customer": row.customer,
            "lead_opportunity": row.opportunity,
            "subject": f"Quotation: {row.name}",
            "status": row.status,
            "reference": row.name,
            "reference_doctype": "Quotation",
            "created_by": row.sales_person,
            "quotation_amount": row.grand_total
        })

    return activities
# =========================================================
# GROUPING
# =========================================================

def apply_grouping(filters, activities):

    group_by = (filters.get("group_by") or "").strip()

    if not group_by:
        return activities

    if group_by == "Sales Person":
        return group_by_sales_person(activities, filters)

    elif group_by == "Activity Type":
        return group_by_activity_type(activities)

    elif group_by == "Client":
        return group_by_client(activities)

    return activities

def group_by_activity_type(activities):

    grouped = defaultdict(lambda: {
        "activity_type": "",
        "total_count": 0,
        "clients": set(),
        "sales_persons": set()
    })

    for row in activities:

        activity = row.get("activity_type") or "Other"

        grouped[activity]["activity_type"] = activity
        grouped[activity]["total_count"] += 1

        if row.get("customer"):
            grouped[activity]["clients"].add(row["customer"])

        if row.get("sales_person"):
            grouped[activity]["sales_persons"].add(row["sales_person"])

    final_data = []

    for activity, values in grouped.items():

        values["unique_clients"] = len(values["clients"])
        values["sales_persons_involved"] = len(values["sales_persons"])

        del values["clients"]
        del values["sales_persons"]

        final_data.append(values)

    return final_data


def group_by_client(activities):

    grouped = defaultdict(lambda: {
        "customer": "",
        "total_activities": 0,
        "phone_calls": 0,
        "emails": 0,
        "meetings": 0,
        "quotations": 0,
        "tasks": 0,
        "last_activity_date": None
    })

    for row in activities:

        customer = row.get("customer") or "Unknown"

        grouped[customer]["customer"] = customer
        grouped[customer]["total_activities"] += 1

        if row["activity_type"] == "Phone Call":
            grouped[customer]["phone_calls"] += 1

        elif row["activity_type"] == "Email":
            grouped[customer]["emails"] += 1

        elif row["activity_type"] == "Meeting":
            grouped[customer]["meetings"] += 1

        elif row["activity_type"] == "Quotation":
            grouped[customer]["quotations"] += 1

        elif row["activity_type"] == "Task":
            grouped[customer]["tasks"] += 1

        if not grouped[customer]["last_activity_date"]:
            grouped[customer]["last_activity_date"] = row.get("date")

        elif row.get("date") > grouped[customer]["last_activity_date"]:
            grouped[customer]["last_activity_date"] = row.get("date")

    return list(grouped.values())
def group_by_sales_person(activities, filters):

    selected_sp = filters.get("sales_person")

    if selected_sp:
        all_sales_users = [selected_sp]
    else:
        all_sales_users = [d[0] for d in frappe.db.sql("""
            SELECT DISTINCT u.name
            FROM `tabUser` u
            INNER JOIN `tabHas Role` hr
                ON hr.parent = u.name
            WHERE hr.role = 'My Activity Report User'
            AND u.enabled = 1
            AND u.name NOT IN (
                'superadmin@boxtech.ai'
            )
            ORDER BY u.name
        """, as_list=True)]

    frappe.log_error(
        title="Sales Team KPI - All Sales Users",
        message=str(all_sales_users)
    )

    grouped = {}

    for user in all_sales_users:
        grouped[user] = {
            "sales_person": user,
            "total_activities": 0,
            "phone_calls": 0,
            "emails": 0,
            "meetings": 0,
            "quotations": 0,
            "tasks": 0,
            "clients": set()
        }

    for row in activities:

        sp = row.get("sales_person") or "Unknown"

        # Skip superadmin completely
        if sp == "superadmin@boxtech.ai":
            continue

        if sp not in grouped:
            grouped[sp] = {
                "sales_person": sp,
                "total_activities": 0,
                "phone_calls": 0,
                "emails": 0,
                "meetings": 0,
                "quotations": 0,
                "tasks": 0,
                "clients": set()
            }

        grouped[sp]["total_activities"] += 1

        if row["activity_type"] == "Phone Call":
            grouped[sp]["phone_calls"] += 1

        elif row["activity_type"] == "Email":
            grouped[sp]["emails"] += 1

        elif row["activity_type"] == "Meeting":
            grouped[sp]["meetings"] += 1

        elif row["activity_type"] == "Quotation":
            grouped[sp]["quotations"] += 1

        elif row["activity_type"] == "Task":
            grouped[sp]["tasks"] += 1

        if row.get("customer"):
            grouped[sp]["clients"].add(row["customer"])

    frappe.log_error(
        title="Sales Team KPI - Grouped Users",
        message=str(list(grouped.keys()))
    )

    final_data = []

    for sp, values in grouped.items():

        values["unique_clients"] = len(values["clients"])
        del values["clients"]

        final_data.append(values)

    frappe.log_error(
        title="Sales Team KPI - Final Data",
        message=str(final_data)
    )

    return final_data

# =========================================================
# SUMMARY
# =========================================================

def get_report_summary(data):

    total_activities = len(data)

    phone_calls = len([
        d for d in data
        if d["activity_type"] == "Phone Call"
    ])

    emails = len([
        d for d in data
        if d["activity_type"] == "Email"
    ])

    meetings = len([
        d for d in data
        if d["activity_type"] == "Meeting"
    ])

    quotations = len([
        d for d in data
        if d["activity_type"] == "Quotation"
    ])

    tasks = len([
        d for d in data
        if d["activity_type"] == "Task"
    ])

    unique_clients = len(set([
        d.get("customer")
        for d in data
        if d.get("customer")
    ]))

    active_sales_persons = len(set([
        d.get("sales_person")
        for d in data
        if d.get("sales_person")
    ]))
    pending_tasks = len([
        d for d in data
        if d.get("status") in ["Pending", "⏳In Progress"]
    ])

    completed_tasks = len([
        d for d in data
        if d.get("status") in ["Completed", "✅Complete"]
    ])

    return [
        {
            "value": total_activities,
            "label": "Total Activities",
            "datatype": "Int",
            "indicator": "Blue"
        },
        {
            "value": phone_calls,
            "label": "Phone Calls",
            "datatype": "Int",
            "indicator": "Green"
        },
        {
            "value": emails,
            "label": "Emails",
            "datatype": "Int",
            "indicator": "Orange"
        },
        {
            "value": meetings,
            "label": "Meetings",
            "datatype": "Int",
            "indicator": "Purple"
        },
        {
            "value": quotations,
            "label": "Quotations",
            "datatype": "Int",
            "indicator": "Blue"
        },
        {
            "value": tasks,
            "label": "Tasks",
            "datatype": "Int",
            "indicator": "Red"
        },
        {
            "value": unique_clients,
            "label": "Unique Clients",
            "datatype": "Int",
            "indicator": "Green"
        },
        {
            "value": active_sales_persons,
            "label": "Active Sales Persons",
            "datatype": "Int",
            "indicator": "Orange"
        },
        {
            "value": pending_tasks,
            "label": "Pending Tasks",
            "datatype": "Int",
            "indicator": "Orange"
        },
        {
            "value": completed_tasks,
            "label": "Completed Tasks",
            "datatype": "Int",
            "indicator": "Green"
        }
    ]


# =========================================================
# CHART
# =========================================================

def get_chart_data(data):

    return None


# =========================================================
# HELPERS
# =========================================================

def classify_communication(row):

    subject = (row.subject or "").lower()

    if "call" in subject:
        return "Phone Call"

    if row.communication_type == "Communication":
        return "Email"

    return "Other"


def get_conditions(filters, sales_person_field="owner"):

    conditions = ""

    if filters.get("sales_person"):
        conditions += f" AND {sales_person_field} = %(sales_person)s "

    return conditions

def normalize_activity_type(activity_type):

    activity_type = (activity_type or "").strip().lower()

    if "call" in activity_type:
        return "Phone Call"

    elif "email" in activity_type:
        return "Email"

    elif (
        "meeting" in activity_type
        or "presentation" in activity_type
        or "visit" in activity_type
    ):
        return "Meeting"

    elif "quotation" in activity_type:
        return "Quotation"

    elif "task" in activity_type:
        return "Task"

    elif "whatsapp" in activity_type:
        return "WhatsApp"

    elif "linkedin" in activity_type:
        return "LinkedIn"

    return "Other"