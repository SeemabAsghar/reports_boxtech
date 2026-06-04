# Copyright (c) 2026, seemabasghar04@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):

    columns = [
        {
            "label": "Manufacturer",
            "fieldname": "manufacturer",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": "Country",
            "fieldname": "country",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 250
        },
        {
            "label": "Devices",
            "fieldname": "devices",
            "fieldtype": "Int",
            "width": 120
        }
    ]

    data = get_data(filters)

    return columns, data


def get_data(filters):

    conditions = ""

    if filters.get("manufacturer"):
        conditions += """
            AND cmd.manufacturer = %(manufacturer)s
        """

    if filters.get("country"):
        conditions += """
            AND c.custom_country = %(country)s
        """

    if filters.get("customer"):
        conditions += """
            AND c.name = %(customer)s
        """

    return frappe.db.sql(
        f"""
        SELECT
            cmd.manufacturer,
            c.custom_country AS country,
            c.name AS customer,
            SUM(cmd.qty_per_month) AS devices

        FROM `tabCustomer Monthly Devices` cmd

        INNER JOIN `tabCustomer` c
            ON c.name = cmd.parent

        WHERE 1=1
        {conditions}

        GROUP BY
            cmd.manufacturer,
            c.custom_country,
            c.name

        ORDER BY
            devices DESC
        """,
        filters,
        as_dict=True
    )