# Copyright (c) 2026, seemabasghar04@gmail.com and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):

    group_by = filters.get("group_by", "Manufacturer")

    if group_by == "Manufacturer":
        columns = [
            {
                "label": "Manufacturer",
                "fieldname": "manufacturer",
                "fieldtype": "Data",
                "width": 250
            },
            {
                "label": "Devices",
                "fieldname": "devices",
                "fieldtype": "Int",
                "width": 120
            }
        ]
    else:
        columns = [
            {
                "label": "Country",
                "fieldname": "country",
                "fieldtype": "Data",
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

    total_devices = sum(row.get("devices", 0) for row in data)

    if group_by == "Manufacturer":
        data.append({
            "manufacturer": "Total",
            "devices": total_devices
        })
    else:
        data.append({
            "country": "Total",
            "devices": total_devices
        })

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

    group_by = filters.get("group_by", "Manufacturer")

    if group_by == "Manufacturer":

        query = f"""
            SELECT
                cmd.manufacturer,
                COALESCE(SUM(cmd.qty_per_month), 0) AS devices

            FROM `tabCustomer Monthly Devices` cmd

            INNER JOIN `tabCustomer` c
                ON c.name = cmd.parent

            WHERE 1=1
            {conditions}

            GROUP BY
                cmd.manufacturer

            ORDER BY
                cmd.manufacturer
        """

    else:

        query = f"""
            SELECT
                c.custom_country AS country,
                COALESCE(SUM(cmd.qty_per_month), 0) AS devices

            FROM `tabCustomer Monthly Devices` cmd

            INNER JOIN `tabCustomer` c
                ON c.name = cmd.parent

            WHERE 1=1
            {conditions}

            GROUP BY
                c.custom_country

            ORDER BY
                c.custom_country
        """

    return frappe.db.sql(query, filters, as_dict=True)