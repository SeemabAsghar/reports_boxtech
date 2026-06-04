// Copyright (c) 2026, seemabasghar04@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Manufacturer Device Summary"] = {

    onload: function(report) {

        report.page.add_inner_button("Clear Filters", function() {

            report.set_filter_value("manufacturer", "");

            report.set_filter_value("country", "");

            report.set_filter_value("customer", "");

            report.set_filter_value("sort_by", "");

            report.refresh();
        });
    },

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
        },
        {
            fieldname: "sort_by",
            label: "Sort By",
            fieldtype: "Select",
            options: "\nManufacturer\nCountry"
        }
    ]
};