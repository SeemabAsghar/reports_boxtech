// Copyright (c) 2026, seemabasghar04@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Stock List"] = {

    onload: function(report) {

        report.page.add_inner_button("Clear Filters", function() {

            report.set_filter_value("manufacturer", "");
            report.set_filter_value("group_by", "");

            report.refresh();
        });
    },

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
            options: "\nManufacturer\nModel"
        }
    ]
};