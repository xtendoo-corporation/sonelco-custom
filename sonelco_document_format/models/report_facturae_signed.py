# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ReportFacturaeTemplate(models.AbstractModel):
    _inherit = "report.l10n_es_facturae.template_facturae"

    @api.model
    def generate_report(self, ir_report, docids, data=None):
        """Override to replace single quotes with double quotes in XML declaration."""
        result, content_type = super().generate_report(ir_report, docids, data=data)
        if isinstance(result, bytes):
            result = result.replace(
                b"<?xml version='1.0' encoding='UTF-8'?>",
                b'<?xml version="1.0" encoding="UTF-8"?>',
            )
        return result, content_type


class ReportFacturaeSigned(models.AbstractModel):
    _inherit = "report.l10n_es_facturae.facturae_signed"

    def _sign_file(self, move, request, public_cert, private_key):
        """Override to replace single quotes with double quotes in XML declaration."""
        result = super()._sign_file(move, request, public_cert, private_key)
        if isinstance(result, bytes):
            result = result.replace(
                b"<?xml version='1.0' encoding='UTF-8'?>",
                b'<?xml version="1.0" encoding="UTF-8"?>',
            )
        return result
