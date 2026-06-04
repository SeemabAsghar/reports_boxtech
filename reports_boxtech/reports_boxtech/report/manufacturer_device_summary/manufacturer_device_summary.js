// Copyright (c) 2026, seemabasghar04@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Manufacturer Device Summary"] = {
    filters: [
        {
            fieldname: "manufacturer",
            label: "Manufacturer",
            fieldtype: "Link",
            options: "Manufacturer"
        },
        {
            fieldname: "country",
            label: "Country",
			fieldtype: "Link",
			options: "Country"
			
        },
        {
            fieldname: "customer",
            label: "Customer",
            fieldtype: "Link",
            options: "Customer"
        }
    ]
};