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
            fieldname: "sort_by",
            label: __("Sort By"),
            fieldtype: "Select",
            options: "\nCurrent Stock\nManufacturer\nModel",
            default: "Current Stock"
        }
    ]
};