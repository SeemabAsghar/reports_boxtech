// Copyright (c) 2026, seemabasghar04@gmail.com and contributors
// For license information, please see license.txt
frappe.query_reports["Stock List"] = {
    filters: [
        {
            fieldname: "manufacturer",
            label: __("Manufacturer"),
            fieldtype: "Link",
			options: "Manufacturer"
        },
        {
            fieldname: "group_by",
            label: __("Group By"),
            fieldtype: "Select",
            options: "\nManufacturer\nModel",
            default: "Manufacturer"
        }
    ]
};