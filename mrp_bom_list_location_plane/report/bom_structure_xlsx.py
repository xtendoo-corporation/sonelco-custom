from odoo import models


class BomStructureXlsx(models.AbstractModel):
    _name = "report.mrp_bom_list_location_plane.report_bom_structure_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "BoM Structure XLSX"

    def _get_variant_id(self, data):
        variant = (data or {}).get("variant")
        if variant in (False, None, "", "false", "False"):
            return False
        return int(str(variant))

    def _get_product(self, bom, data):
        variant_id = self._get_variant_id(data)
        if variant_id:
            return self.env["product.product"].browse(variant_id)
        return (
            bom.product_id
            or bom.product_tmpl_id.product_variant_id
            or bom.product_tmpl_id.product_variant_ids[:1]
        )

    def _get_requested_quantity(self, bom, data):
        return float((data or {}).get("quantity") or bom.product_qty or 1.0)

    def _get_title(self, bom, product):
        default_code = product.default_code or bom.product_tmpl_id.default_code or ""
        name = product.name or bom.product_tmpl_id.name or bom.display_name
        if default_code:
            return f"{default_code} ({name})"
        return name

    def _sheet_name(self, title):
        return (title or "BoM")[:31]

    def _get_scaled_quantity(self, bom, bom_line, requested_qty):
        base_qty = bom.product_qty or 1.0
        factor = requested_qty / base_qty
        return bom_line.product_qty * factor

    def generate_xlsx_report(self, workbook, data, boms):
        for bom in boms:
            product = self._get_product(bom, data)
            requested_qty = self._get_requested_quantity(bom, data)
            title = self._get_title(bom, product)

            sheet = workbook.add_worksheet(self._sheet_name(title))

            title_format = workbook.add_format({
                "bold": True,
                "font_size": 18,
                "align": "center",
                "valign": "vcenter",
            })
            header_format = workbook.add_format({
                "bold": True,
                "bg_color": "#FFF9C4",
                "border": 1,
                "align": "left",
                "valign": "vcenter",
            })
            text_format = workbook.add_format({
                "border": 1,
                "valign": "vcenter",
            })
            qty_format = workbook.add_format({
                "border": 1,
                "align": "right",
                "valign": "vcenter",
                "num_format": "#,##0.####",
            })
            blank_format = workbook.add_format({
                "border": 1,
                "valign": "vcenter",
            })

            sheet.set_row(0, 30)
            sheet.set_row(1, 24)

            sheet.set_column(0, 0, 16)
            sheet.set_column(1, 1, 22)
            sheet.set_column(2, 2, 95)
            sheet.set_column(3, 3, 12)

            sheet.merge_range(0, 0, 0, 3, title, title_format)

            headers = ["Location", "Product Reference", "Product Name", "Quantity"]
            for col, header in enumerate(headers):
                sheet.write(1, col, header, header_format)

            sheet.write_blank(2, 0, None, blank_format)
            sheet.write_blank(2, 1, None, blank_format)
            sheet.write_blank(2, 2, None, blank_format)
            sheet.write_number(2, 3, requested_qty, qty_format)

            row = 3
            for bom_line in bom.bom_line_ids.sorted(key=lambda l: (l.sequence, l.id)):
                product_ref = bom_line.product_id.default_code or bom_line.product_tmpl_id.default_code or ""
                product_name = bom_line.product_id.display_name or bom_line.product_tmpl_id.display_name or ""
                quantity = self._get_scaled_quantity(bom, bom_line, requested_qty)

                sheet.write(row, 0, bom_line.location_plane or "", text_format)
                sheet.write(row, 1, product_ref, text_format)
                sheet.write(row, 2, product_name, text_format)
                sheet.write_number(row, 3, quantity, qty_format)
                row += 1

