# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, models
from odoo.tools import cleanup_xml_node


class ReportXmlAbstract(models.AbstractModel):
    """
    Extend report.report_xml.abstract to ensure XML declaration
    uses double quotes instead of single quotes.
    """

    _inherit = "report.report_xml.abstract"

    @api.model
    def generate_report(self, ir_report, docids, data=None):
        xml_content, content_type = super().generate_report(
            ir_report, docids, data=data
        )

        tree = cleanup_xml_node(xml_content)

        encoding = ir_report.xml_encoding or "UTF-8"
        xml_content = etree.tostring(
            tree,
            xml_declaration=False,
            encoding=encoding,
            pretty_print=True,
        )

        if ir_report.xml_declaration:
            declaration = f'<?xml version="1.0" encoding="{encoding}"?>\n'.encode(
                encoding
            )
            xml_content = declaration + xml_content

        return xml_content, content_type
