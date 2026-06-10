# Copyright (c) 2026, seemabasghar04@gmail.com and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)

    return columns, data
def get_columns(filters):

    group_by = filters.get("group_by")

    if not group_by:
        return [
            {
                "label": "Manufacturer",
                "fieldname": "manufacturer",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": "Category",
                "fieldname": "item_group",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": "Type",
                "fieldname": "description",
                "fieldtype": "Data",
                "width": 350
            },
            {
                "label": "Model",
                "fieldname": "item_code",
                "fieldtype": "Link",
                "options": "Item",
                "width": 180
            },
            {
                "label": "Current Stock",
                "fieldname": "current_stock",
                "fieldtype": "Float",
                "width": 140
            }
        ]

    elif group_by == "Manufacturer":
        return [
            {
                "label": "Manufacturer",
                "fieldname": "manufacturer",
                "fieldtype": "Data",
                "width": 250
            },
            {
                "label": "Current Stock",
                "fieldname": "current_stock",
                "fieldtype": "Float",
                "width": 150
            }
        ]

    else:
        return [
            {
                "label": "Model",
                "fieldname": "item_code",
                "fieldtype": "Link",
                "options": "Item",
                "width": 250
            },
            {
                "label": "Current Stock",
                "fieldname": "current_stock",
                "fieldtype": "Float",
                "width": 150
            }
        ]
        
def get_data(filters):

    conditions = ""

    if filters.get("manufacturer"):
        conditions += """
            AND im.manufacturer = %(manufacturer)s
        """

    group_by = filters.get("group_by")

    if not group_by:

        query = f"""
            SELECT
                COALESCE(im.manufacturer, '') AS manufacturer,
                i.item_group,
                i.description,
                i.item_code,
                COALESCE(SUM(b.actual_qty), 0) AS current_stock

            FROM `tabItem` i

            LEFT JOIN `tabItem Manufacturer` im
                ON im.item_code = i.item_code
                AND im.is_default = 1

            LEFT JOIN `tabBin` b
                ON b.item_code = i.item_code

            WHERE
                i.disabled = 0
                {conditions}

            GROUP BY
                i.item_code,
                i.item_group,
                i.description,
                im.manufacturer

            ORDER BY
                current_stock DESC
        """

    elif group_by == "Manufacturer":

        query = f"""
            SELECT
                COALESCE(im.manufacturer, '') AS manufacturer,
                COALESCE(SUM(b.actual_qty), 0) AS current_stock

            FROM `tabItem` i

            LEFT JOIN `tabItem Manufacturer` im
                ON im.item_code = i.item_code
                AND im.is_default = 1

            LEFT JOIN `tabBin` b
                ON b.item_code = i.item_code

            WHERE
                i.disabled = 0
                {conditions}

            GROUP BY
                im.manufacturer

            ORDER BY
                im.manufacturer
        """

    else:

        query = f"""
            SELECT
                i.item_code,
                COALESCE(SUM(b.actual_qty), 0) AS current_stock

            FROM `tabItem` i

            LEFT JOIN `tabItem Manufacturer` im
                ON im.item_code = i.item_code
                AND im.is_default = 1

            LEFT JOIN `tabBin` b
                ON b.item_code = i.item_code

            WHERE
                i.disabled = 0
                {conditions}

            GROUP BY
                i.item_code

            ORDER BY
                i.item_code
        """

    return frappe.db.sql(query, filters, as_dict=True)