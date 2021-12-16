from odoo import models, fields, api, _


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    property_delivery_carrier_id = fields.Many2one(
        comodel_name='delivery.carrier',
        company_dependent=True,
        string="Delivery Method",
        help="Default delivery method."
    )
    package = fields.Float(
        string="Number of package",
        digits=(16, 0),
    )
