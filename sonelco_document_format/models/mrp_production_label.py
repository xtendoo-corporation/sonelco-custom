import re
from datetime import date

from odoo import api, models


class ReportMrpProductionLabel(models.AbstractModel):
    """Helper model for the 3 MRP production label reports."""

    _name = "report.sonelco_document_format.mrp_label_serial_template"
    _description = "MRP Production – Etiqueta Serie (Sn)"

    @api.model
    def _get_report_values(self, docids, data=None):
        productions = self.env["mrp.production"].browse(docids)
        return {
            "docs": productions,
            "get_serial_lines": self._get_serial_lines,
            "get_lot_code": self._get_lot_code,
        }

    @staticmethod
    def _extract_mo_number(production_name):
        """Extract the numeric suffix from an MO reference.

        E.g. 'WH/MO/00012614' → '12614'
             'MO/00012614'     → '12614'
             '12614'           → '12614'
        """
        digits = re.findall(r"\d+", production_name or "")
        if digits:
            # Concatenate all digit groups and strip leading zeros.
            raw = "".join(digits)
            return str(int(raw)) if raw else "0"
        return "0"

    @classmethod
    def _get_serial_lines(cls, production):

        mo_num = cls._extract_mo_number(production.name)

        sequences = max(1, int(production.product_qty or 1))

        # Sum quantities of all non-cancelled raw material moves ignoring < 1
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

            # Last sequence absorbs any remainder
            copies_to_print = base_copies_per_seq
            if seq == sequences:
                copies_to_print += remainder

            for _copy in range(copies_to_print):
                lines.append({"code": code, "barcode_value": code})

        return lines

    @staticmethod
    def _get_lot_code(production):
        """Compute the Ln code for the given production order.

        Format: Ln + YY + WW + last4_EAN + version
        Example: Ln265362502
            YY   = 26 (year 2026, last 2 digits)
            WW   = 53 (ISO week, zero-padded to 2)
            last4= 6250 (last 4 digits of barcode)
            ver  = 2   (x_version)
        """
        today = date.today()
        yy = str(today.year)[-2:]
        ww = f"{today.isocalendar()[1]:02d}"
        barcode = production.product_id.barcode or ""
        last4 = barcode[-4:] if len(barcode) >= 4 else barcode.zfill(4)
        version = production.product_id.x_version or ""
        code = f"Ln{yy}{ww}{last4}{version}"
        return {"code": code, "barcode_value": code}
