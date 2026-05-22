// Copyright (c) 2026, seemabasghar04@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Team KPIs"] = {

    onload: function(report) {

        report.page.add_inner_button("Clear Filters", function() {

            report.set_filter_value("from_date", frappe.datetime.month_start());

            report.set_filter_value("to_date", frappe.datetime.month_end());

            report.set_filter_value("activity_type", "All Activities");

            report.set_filter_value("sales_person", "");

            report.set_filter_value("customer", "");

            report.set_filter_value("status", "");

            report.set_filter_value("group_by", "");

            report.refresh();
        });
    },

    filters: [

        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            default: frappe.datetime.month_start()
        },

        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            default: frappe.datetime.month_end()
        },

        {
            fieldname: "activity_type",
            label: "Activity Type",
            fieldtype: "Select",
            options: "\nAll Activities\nPhone Call\nEmail\nMeeting\nQuotation\nTask\nWhatsApp\nLinkedIn\nOther",
            default: "All Activities"
        },

        {
            fieldname: "sales_person",
            label: "Sales Person",
            fieldtype: "Link",
            options: "User"
        },

        {
            fieldname: "customer",
            label: "Customer / Client",
            fieldtype: "Link",
            options: "Customer"
        },

        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: "\nPending\nCompleted\n⏳In Progress\n✅Complete\nOpen\nClosed\nCancelled\nDraft"
        },

        {
            fieldname: "group_by",
            label: "Group By",
            fieldtype: "Select",
            options: "\nSales Person\nActivity Type\nClient"
        }
    ]
};