import re
from datetime import date

from odoo import api, models


def extract_mo_number(production_name):
    """Extract the numeric suffix from an MO reference."""
    digits = re.findall(r"\d+", production_name or "")
    if digits:
        raw = "".join(digits)
        return str(int(raw)) if raw else "0"
    return "0"


def get_serial_lines(production):
    mo_num = extract_mo_number(production.name)
    sequences = max(1, int(production.product_qty or 1))

    total_valid_bom_qty = sum(
        move.product_qty
        for move in production.move_raw_ids
        if move.state != "cancel" and move.product_qty >= 1
    )

    total_labels = int(total_valid_bom_qty)
    base_copies_per_seq = total_labels // sequences
    remainder = total_labels % sequences

    lines = []
    for seq in range(1, sequences + 1):
        code = f"Sn{mo_num}{seq:04d}"
        copies_to_print = base_copies_per_seq
        if seq == sequences:
            copies_to_print += remainder
        for _copy in range(copies_to_print):
            lines.append({"code": code, "barcode_value": code})
    return lines


def get_lot_code(production):
    """Compute the Ln code for the given production order."""
    today = date.today()
    yy = str(today.year)[-2:]
    ww = f"{today.isocalendar()[1]:02d}"
    barcode = production.product_id.barcode or ""
    last4 = barcode[-4:] if len(barcode) >= 4 else barcode.zfill(4)
    version = production.product_id.x_version or ""
    code = f"Ln{yy}{ww}{last4}{version}"
    return {"code": code, "barcode_value": code}


class ReportMrpProductionLabelSerial(models.AbstractModel):
    _name = "report.sonelco_document_format.mrp_label_serial_template"
    _description = "MRP Production – Etiqueta Serie (Sn)"

    @api.model
    def _get_report_values(self, docids, data=None):
        productions = self.env["mrp.production"].browse(docids)
        return {
            "docs": productions,
            "get_serial_lines": get_serial_lines,
        }


class ReportMrpProductionLabelLot(models.AbstractModel):
    _name = "report.sonelco_document_format.mrp_label_lot_template"
    _description = "MRP Production – Etiqueta Lote (Ln)"

    @api.model
    def _get_report_values(self, docids, data=None):
        productions = self.env["mrp.production"].browse(docids)
        return {
            "docs": productions,
            "get_lot_code": get_lot_code,
        }


class ReportMrpProductionLabelProduct(models.AbstractModel):
    _name = "report.sonelco_document_format.mrp_label_product_template"
    _description = "MRP Production – Etiqueta Producto"

    @api.model
    def _get_report_values(self, docids, data=None):
        productions = self.env["mrp.production"].browse(docids)
        return {
            "docs": productions,
            "get_lot_code": get_lot_code,
        }
