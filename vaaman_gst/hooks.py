app_name = "vaaman_gst"
app_title = "vaaman_gst"
app_publisher = "Shalindra Aporiya"
app_description = "This is gst app "
app_email = "shalidnra.aporiya@octavision.in"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "vaaman_gst",
# 		"logo": "/assets/vaaman_gst/logo.png",
# 		"title": "vaaman_gst",
# 		"route": "/vaaman_gst",
# 		"has_permission": "vaaman_gst.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vaaman_gst/css/vaaman_gst.css"
# app_include_js = "/assets/vaaman_gst/js/vaaman_gst.js"
# app_include_js = "/assets/vaaman_gst/js/vaaman_gst.js"

# include js, css files in header of web template
# web_include_css = "/assets/vaaman_gst/css/vaaman_gst.css"
# web_include_js = "/assets/vaaman_gst/js/vaaman_gst.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "vaaman_gst/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Purchase Invoice": "public/js/match_status.js",
    "Purchase Reconciliation Tool": "public/js/purchase_reconciliation_tool.js",
}
# doctype_list_js = {"Purchase Reconciliation Tool" : "public/js/purchase_reconciliation.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "vaaman_gst/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "vaaman_gst.utils.jinja_methods",
# 	"filters": "vaaman_gst.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "vaaman_gst.install.before_install"
# after_install = "vaaman_gst.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "vaaman_gst.uninstall.before_uninstall"
# after_uninstall = "vaaman_gst.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "vaaman_gst.utils.before_app_install"
# after_app_install = "vaaman_gst.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "vaaman_gst.utils.before_app_uninstall"
# after_app_uninstall = "vaaman_gst.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vaaman_gst.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"Purchase Invoice": {
# 		"before_submit": "vaaman_gst.vaaman_gst.match_status.set_match_status"
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"vaaman_gst.tasks.all"
# 	],
# 	"daily": [
# 		"vaaman_gst.tasks.daily"
# 	],
# 	"hourly": [
# 		"vaaman_gst.tasks.hourly"
# 	],
# 	"weekly": [
# 		"vaaman_gst.tasks.weekly"
# 	],
# 	"monthly": [
# 		"vaaman_gst.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "vaaman_gst.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "vaaman_gst.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "vaaman_gst.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["vaaman_gst.utils.before_request"]
# after_request = ["vaaman_gst.utils.after_request"]

# Job Events
# ----------
# before_job = ["vaaman_gst.utils.before_job"]
# after_job = ["vaaman_gst.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"vaaman_gst.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

# override_doctype_class = {
#     "Purchase Reconciliation Tool": "vaaman_gst.overrides.purchase_reconciliation_tool.PurchaseReconciliationTool"
# }

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": {
            "name": [
                "in", [
                    "Purchase Invoice-custom_match_status"
                ]
            ]
        }
    }
]

# Excel column layout is customized by patching BuildExcel in vaaman_gst/__init__.py
# (get_invoice_columns lives on BuildExcel, not on the Purchase Reconciliation Tool DocType).