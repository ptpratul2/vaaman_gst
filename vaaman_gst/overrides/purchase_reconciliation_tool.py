

import importlib
import re
import json
import frappe
from frappe import _

from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
    get_accounting_dimensions,
)
from india_compliance.gst_india.doctype.purchase_reconciliation_tool.purchase_reconciliation_tool import (
    BuildExcel,
    ExcelExporter,
    ReconciledData,
    parse_params,
)

PRT_MODULE = "india_compliance.gst_india.doctype.purchase_reconciliation_tool.purchase_reconciliation_tool"

# Openpyxl rejects these in a cell (XML 1.0 illegal characters). A form-feed
# copied into Supplier.supplier_name was aborting the whole workbook.
_ILLEGAL_EXCEL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def excel_safe(value):
    if isinstance(value, str):
        return _ILLEGAL_EXCEL_CHARS.sub("", value)
    return value


class CustomBuildExcel(BuildExcel):
    @parse_params
    def __init__(self, doc, data, is_supplier_specific=False, email=False, selected_columns=None):
        self.doc = doc
        self.data = data
        self.is_supplier_specific = is_supplier_specific
        self.email = email
        
        if isinstance(selected_columns, str):
            try: self.selected_columns = json.loads(selected_columns)
            except: self.selected_columns = None
        else:
            self.selected_columns = selected_columns

        self.set_headers()
        self.set_filters()

    def get_supplier_columns(self):
        """Standard + missing count columns for Summary Sheet"""
        columns = super().get_supplier_columns()
        
        # Ensure Summary Sheet has all count fields
        extra_summary_cols = [
            {"label": "Differences", "fieldname": "differences", "data_format": {"bg_color": self.COLOR_PALLATE.light_pink}}
        ]
        columns.extend(extra_summary_cols)
        return columns

    def get_invoice_columns(self):
        """Full list of all requested columns with proper data formats"""
        self.dimension_fields = ["project", "cost_center"] + get_accounting_dimensions()
        dimension_columns = [
            {"label": frappe.unscrub(dimension), "fieldname": dimension, "data_format": {"horizontal": "left"}}
            for dimension in self.dimension_fields
        ]

        # 1. Purchase Side (Green Side)
        self.pr_columns = [
            {"label": "Bill No", "fieldname": "bill_no", "compare_with": "inward_supply_bill_no", "data_format": {"bg_color": self.COLOR_PALLATE.light_green}},
            {"label": "Bill Date", "fieldname": "bill_date", "compare_with": "inward_supply_bill_date", "data_format": {"bg_color": self.COLOR_PALLATE.light_green}},
            {"label": "GSTIN", "fieldname": "supplier_gstin", "compare_with": "inward_supply_supplier_gstin", "data_format": {"bg_color": self.COLOR_PALLATE.light_green}},
            {"label": "Place of Supply", "fieldname": "place_of_supply", "compare_with": "inward_supply_place_of_supply", "data_format": {"bg_color": self.COLOR_PALLATE.light_green}},
            {"label": "Reverse Charge", "fieldname": "is_reverse_charge", "compare_with": "inward_supply_is_reverse_charge", "data_format": {"bg_color": self.COLOR_PALLATE.light_green}},
            {"label": "Taxable Value", "fieldname": "taxable_value", "compare_with": "inward_supply_taxable_value", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_green, "number_format": "0.00"}},
            {"label": "CGST", "fieldname": "cgst", "compare_with": "inward_supply_cgst", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_green , "number_format": "0.00"}},
            {"label": "SGST", "fieldname": "sgst", "compare_with": "inward_supply_sgst", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_green, "number_format": "0.00"}},
            {"label": "IGST", "fieldname": "igst", "compare_with": "inward_supply_igst", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_green, "number_format": "0.00"}},
            {"label": "CESS", "fieldname": "cess", "compare_with": "inward_supply_cess", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_green, "number_format": "0.00"}},
        ]

        # 2. Inward Supply Side (Blue Side)
        self.inward_supply_columns = [
            {"label": "IS Bill No", "fieldname": "inward_supply_bill_no", "compare_with": "bill_no", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue}},
            {"label": "IS Bill Date", "fieldname": "inward_supply_bill_date", "compare_with": "bill_date", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue}},
            {"label": "IS GSTIN", "fieldname": "inward_supply_supplier_gstin", "compare_with": "supplier_gstin", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue}},
            {"label": "IS Place of Supply", "fieldname": "inward_supply_place_of_supply", "compare_with": "place_of_supply", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue}},
            {"label": "IS Reverse Charge", "fieldname": "inward_supply_is_reverse_charge", "compare_with": "is_reverse_charge", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue}},
            {"label": "IS Taxable Value", "fieldname": "inward_supply_taxable_value", "compare_with": "taxable_value", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue, "number_format": "0.00"}},
            {"label": "IS CGST", "fieldname": "inward_supply_cgst", "compare_with": "cgst", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue, "number_format": "0.00"}},
            {"label": "IS SGST", "fieldname": "inward_supply_sgst", "compare_with": "sgst", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue, "number_format": "0.00"}},
            {"label": "IS IGST", "fieldname": "inward_supply_igst", "compare_with": "igst", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue , "number_format": "0.00"}},
            {"label": "IS CESS", "fieldname": "inward_supply_cess", "compare_with": "cess", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_blue, "number_format": "0.00"}},
        ]

        # 3. Common Info Columns
        inv_columns = [
            {"label": "Action Status", "fieldname": "action"},
            {"label": "Match Status", "fieldname": "match_status"},
            {"label": "Supplier Name", "fieldname": "supplier_name"},
            {"label": "PAN", "fieldname": "pan", "data_format": {"horizontal": "center"}},
            {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date" , "data_format": {"horizontal": "center"}},
            {"label": "Classification", "fieldname": "classification", "data_format": {"horizontal": "center"}},
            *dimension_columns,
            {"label": "Inward Supply Doc", "fieldname": "inward_supply_name"},
            {"label": "Purchase Doc", "fieldname": "purchase_invoice_name"},
            {"label": "Taxable Value Diff", "fieldname": "taxable_value_difference", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_pink}},
            {"label": "Tax Diff", "fieldname": "tax_difference", "fieldtype": "Float", "data_format": {"bg_color": self.COLOR_PALLATE.light_pink}},
            {"label": "Differences", "fieldname": "differences", "data_format": {"bg_color": self.COLOR_PALLATE.light_pink, "width": 25}},
        ]

        inv_columns.extend(self.inward_supply_columns)
        inv_columns.extend(self.pr_columns)
        return inv_columns

    def get_invoice_data(self):
        """Fixing PAN data and ensuring all column values are populated"""
        data = ReconciledData(**self.doc).get_consolidated_data(
            self.data.get("purchases"),
            self.data.get("inward_supplies"),
            prefix="inward_supply",
        )
        if not data: return []

        # Get extra ERP data
        invoice_names = [d.get("purchase_invoice_name") for d in data if d.get("purchase_invoice_name")]
        pi_map = {}
        if invoice_names:
            invoices = frappe.get_all("Purchase Invoice", 
                filters={"name": ["in", invoice_names]}, 
                fields=["name", "posting_date", "tax_id"])
            pi_map = {d.name: d for d in invoices}

        for row in data:
            # --- PAN FIX ---
            # Extract PAN from GSTIN (3rd to 12th char) if GSTIN exists
            gstin = row.get("supplier_gstin") or row.get("inward_supply_supplier_gstin")
            if gstin and len(gstin) >= 12:
                row["pan"] = gstin[2:12]
            else:
                # Fallback to ERP tax_id if GSTIN is not proper
                row["pan"] = pi_map.get(row.get("purchase_invoice_name"), {}).get("tax_id")

            # --- POSTING DATE ---
            row["posting_date"] = pi_map.get(row.get("purchase_invoice_name"), {}).get("posting_date")

            # --- DIFFERENCES STRING ---
            diff_list = []
            if abs(row.get("taxable_value_difference") or 0) > 1: diff_list.append("Taxable Value")
            if abs(row.get("tax_difference") or 0) > 1: diff_list.append("Tax Amount")
            if row.get("bill_no") != row.get("inward_supply_bill_no"): diff_list.append("Bill No")
            row["differences"] = ", ".join(diff_list) if diff_list else "Match"

        self.supplier_name = excel_safe(
            re.sub(r"[<>[\]?:|*]", "", data[0].get("supplier_name") or "")
        )
        # Envelope email names the file "{supplier}_{gstin}". The core get_file_name
        # reads both attributes; this override was only setting the name.
        self.supplier_gstin = (
            data[0].get("supplier_gstin") or data[0].get("inward_supply_supplier_gstin") or ""
        )
        return self.process_data(data, self.invoice_header)

    def assign_value(self, field, source_data, target_data):
        super().assign_value(field, source_data, target_data)
        target_data[field] = excel_safe(target_data.get(field))

    def set_headers(self):
        """Filter headers and prevent openpyxl crashes"""
        self.match_summary_header = self.get_match_summary_columns()
        self.supplier_header = self.get_supplier_columns()
        self.invoice_header = self.get_invoice_columns()

        if self.selected_columns:
            selected_fields = [c['value'] if isinstance(c, dict) else c for c in self.selected_columns]
            # Essential system fields
            selected_fields.extend(["purchase_invoice_name", "inward_supply_name"])

            self.match_summary_header = [h for h in self.match_summary_header if h['fieldname'] in selected_fields]
            self.supplier_header = [h for h in self.supplier_header if h['fieldname'] in selected_fields]
            self.invoice_header = [h for h in self.invoice_header if h['fieldname'] in selected_fields]

        # Fix TypeError: Remove compare_with if target field is missing
        active_fields = [h['fieldname'] for h in self.invoice_header]
        for h in self.invoice_header:
            if h.get("compare_with") and h.get("compare_with") not in active_fields:
                del h["compare_with"]
                if "data_format" in h and "bg_color" in h["data_format"]:
                    del h["data_format"]["bg_color"]

    def export_data(self):
        """Final sheet generation"""
        excel = ExcelExporter()
        
        # 1. Match Summary
        excel.create_sheet(
            sheet_name="Match Summary Data",
            headers=self.match_summary_header,
            data=self.get_match_summary_data(),
            default_data_format={"bg_color": self.COLOR_PALLATE.light_gray},
            default_header_format={"bg_color": self.COLOR_PALLATE.dark_gray},
        )

        # 2. Supplier Summary
        if not self.is_supplier_specific:
            excel.create_sheet(
                sheet_name="Supplier Data",
                headers=self.supplier_header,
                data=self.get_supplier_data(),
                default_data_format={"bg_color": self.COLOR_PALLATE.light_gray},
                default_header_format={"bg_color": self.COLOR_PALLATE.dark_gray},
            )

        # 3. Invoice Data
        m_headers = None if self.selected_columns else self.get_merge_headers()
        excel.create_sheet(
            sheet_name="Invoice Data",
            merged_headers=m_headers,
            headers=self.invoice_header,
            data=self.get_invoice_data(),
            default_data_format={"bg_color": self.COLOR_PALLATE.light_gray},
            default_header_format={"bg_color": self.COLOR_PALLATE.dark_gray},
        )

        excel.remove_sheet("Sheet")
        file_name = self.get_file_name()
        if self.email: return [excel.save_workbook(), file_name]
        
        excel.export(file_name)

@frappe.whitelist()
def download_excel_report(data, doc, is_supplier_specific=False, selected_columns=None):
    frappe.has_permission("Purchase Reconciliation Tool", "export", throw=True)
    builder = CustomBuildExcel(doc, data, is_supplier_specific, selected_columns=selected_columns)
    builder.export_data()

def patch_build_excel():
    module = importlib.import_module(PRT_MODULE)
    module.BuildExcel = CustomBuildExcel
    module.download_excel_report = download_excel_report


def _same_company_gstin(purchase, inward_supply):
    return (purchase.get("company_gstin") or "") == (inward_supply.get("company_gstin") or "")


def patch_company_gstin_match():
    """Do not pair a 2A/2B row with a purchase booked on a different company GSTIN.

    The standard mismatch rules ignore company GSTIN, so a filing on one
    registration is linked to a purchase on another. Those rows should stay
    Only in 2A/2B and Only in Books.
    """
    import sys

    from india_compliance.gst_india.doctype.purchase_reconciliation_tool import Reconciler
    from india_compliance.gst_india.doctype.purchase_reconciliation_tool import (
        purchase_reconciliation_utils as utils,
    )

    if not getattr(Reconciler.is_doc_matching, "_vaaman_company_gstin_guard", False):
        original_is_doc_matching = Reconciler.is_doc_matching

        def is_doc_matching(self, purchase, inward_supply, rules):
            if not _same_company_gstin(purchase, inward_supply):
                return False
            return original_is_doc_matching(self, purchase, inward_supply, rules)

        is_doc_matching._vaaman_company_gstin_guard = True
        Reconciler.is_doc_matching = is_doc_matching

    if getattr(utils.link_documents, "_vaaman_company_gstin_guard", False):
        return

    original_link_documents = utils.link_documents

    def link_documents(purchase_invoice_name, inward_supply_name, link_doctype):
        if purchase_invoice_name and inward_supply_name and link_doctype:
            purchase_gstin = frappe.db.get_value(link_doctype, purchase_invoice_name, "company_gstin")
            inward_gstin = frappe.db.get_value("GST Inward Supply", inward_supply_name, "company_gstin")
            if (purchase_gstin or "") != (inward_gstin or ""):
                frappe.throw(
                    _(
                        "Cannot match these documents. The purchase is booked on GSTIN {0}, "
                        "but the 2A/2B document is reported on GSTIN {1}."
                    ).format(purchase_gstin or _("blank"), inward_gstin or _("blank"))
                )
        return original_link_documents(purchase_invoice_name, inward_supply_name, link_doctype)

    link_documents._vaaman_company_gstin_guard = True
    utils.link_documents = link_documents

    for module_name in (
        PRT_MODULE,
        "india_compliance.gst_india.doctype.gst_invoice_management_system.gst_invoice_management_system",
    ):
        module = sys.modules.get(module_name)
        if module is not None and hasattr(module, "_link_documents"):
            module._link_documents = link_documents

