# Copyright (c) 2026, seemabasghar04@gmail.com and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
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


def get_data(filters):

    conditions = ""

    if filters.get("manufacturer"):
        conditions += """
            AND im.manufacturer = %(manufacturer)s
        """

    order_by = "current_stock DESC"

    if filters.get("sort_by") == "Manufacturer":
        order_by = "im.manufacturer ASC"

    elif filters.get("sort_by") == "Model":
        order_by = "i.item_code ASC"

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
            {order_by}
    """

    return frappe.db.sql(query, filters, as_dict=True)