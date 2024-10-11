from odoo import models, fields, api, _


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    package = fields.Float(
        string="Number of package",
        digits=(16, 0),
    )
    delivery_id = fields.Many2one(
        comodel_name='stock.picking',
        string='Delivery',
        compute="_compute_delivery_id",
        default=lambda self: self._get_delivery_id(),
        store=True,
    )
    partner_id = fields.Many2one(
        related="delivery_id.partner_id",
        string="Delivery Partner",
    )
    property_delivery_carrier_id = fields.Many2one(
        comodel_name='delivery.carrier',
        company_dependent=True,
        string="Delivery Method",
        help="Package delivery method.",
    )

    @api.depends("quant_ids")
    def _compute_delivery_id(self):
        self.delivery_id = self._get_delivery_id()
        self.property_delivery_carrier_id = self.partner_id.property_delivery_carrier_id

    def _get_delivery_id(self):
        delivery_id = False
        domain = ['|', ('result_package_id', 'in', self.ids), ('package_id', 'in', self.ids)]
        move_line = self.env['stock.move.line'].search(domain)
        if move_line:
            delivery_id = self.env['stock.picking'].search(
                [('id', '=', move_line[0].picking_id.id)],
                limit=1,
            )
        return delivery_id
