// Frappe 16 dropped Font Awesome from the desk bundle. India Compliance still
// renders these action buttons with <i class="fa fa-...">, so the glyphs never
// paint. This file is appended to the same form script, so this declaration
// replaces get_icon before the tables render. Button classes stay the same
// because the click handlers select .btn.eye, .btn.download and .btn.envelope.
function get_icon(value, column, data, icon) {
    const icons = {
        eye: { name: "eye", title: __("View Details") },
        download: { name: "download", title: __("Download") },
        envelope: { name: "mail", title: __("Email") },
    };
    const mapped = icons[icon] || { name: icon, title: icon };
    const hash = get_hash(data);

    return `<button type="button" class="btn icon-btn ${icon}" data-name="${hash}" title="${frappe.utils.escape_html(mapped.title)}">
        ${frappe.utils.icon(mapped.name, "sm")}
    </button>`;
}

frappe.ui.form.on("Purchase Reconciliation Tool", {
    refresh: function(frm) {
        // PurchaseReconciliationToolAction class ko override karein
        if (typeof PurchaseReconciliationToolAction !== 'undefined') {
            
            PurchaseReconciliationToolAction.prototype.export_data = function(selected_row) {
                const reco = this.frm.reconciliation_tabs;
                let all_keys = new Set();

        const python_fieldnames = [
            // Basic Info
            "action", "match_status", "supplier_name", "pan", "classification",
            "inward_supply_name", "purchase_invoice_name", "taxable_value_difference", "tax_difference",
            // Inward Supply (2A/2B) Columns
            "inward_supply_bill_no", "inward_supply_bill_date", "inward_supply_supplier_gstin",
            "inward_supply_place_of_supply", "inward_supply_is_reverse_charge",
            "inward_supply_taxable_value", "inward_supply_cgst", "inward_supply_sgst",
            "inward_supply_igst", "inward_supply_cess",
            // Purchase Data Columns
            "bill_no", "bill_date", "supplier_gstin", "place_of_supply",
            "is_reverse_charge", "taxable_value", "cgst", "sgst", "igst", "cess",
            // Summary Columns
            "inward_supply_count", "purchase_count", "action_taken_count", "total_docs",
            "taxable_value_difference", "tax_difference", "posting_date"
        ];
        python_fieldnames.forEach(f => all_keys.add(f));

        // 2. Scan Raw Data for any Custom Fields or Accounting Dimensions
        const raw_data = reco.data || [];
        raw_data.forEach(row => {
            Object.keys(row).forEach(key => {
                if (!["__unsaved", "doctype", "name", "idx"].includes(key) && !key.startsWith('_')) {
                    all_keys.add(key);
                }
            });
        });

        let sorted_columns = Array.from(all_keys).sort();
        const data_to_export = reco.get_filtered_data(selected_row);

        let d = new frappe.ui.Dialog({
            title: __('Select Columns to Export'),
            size: 'large',
            fields: [
                {
                    label: __('Select Columns'),
                    fieldname: 'selected_columns',
                    fieldtype: 'MultiCheck',
                    options: sorted_columns.map(col => ({
                        label: __(frappe.model.unscrub(col)), 
                        value: col,
                        checked: 1 
                    })),
                    columns: 3 
                }
            ],
            primary_action_label: __('Download Excel'),
            primary_action: (values) => {
                const selected = d.get_field('selected_columns').get_checked_options();
                if (selected.length === 0) {
                    frappe.msgprint(__("Please select at least one column."));
                    return;
                }



                frappe.show_progress(__("Preparing Excel..."), 0, 100, __("Exporting"));
                const url = "vaaman_gst.overrides.purchase_reconciliation_tool.download_excel_report";
                open_url_post(`/api/method/${url}`, {

                    data: JSON.stringify(data_to_export),
                    doc: JSON.stringify(this.frm.doc),
                    is_supplier_specific: !!selected_row,
                    selected_columns: JSON.stringify(selected)
                });

                setTimeout(() => frappe.hide_progress(), 2000);
                d.hide();
            },
            secondary_action_label: __('Cancel'),
            secondary_action: () => d.hide()
        });
        d.show();

            };

            // Setup actions ko refresh karein naye prototype ke sath
            frm.reco_tool_actions = new PurchaseReconciliationToolAction(frm);
            frm.reco_tool_actions.setup_actions();
        }
    }
});