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
        for package in self:
            package.delivery_id = package._get_delivery_id()
            package.property_delivery_carrier_id = (
                package.partner_id.property_delivery_carrier_id
            )

    def _get_delivery_id(self):
        self.ensure_one()
        move_line = self.env['stock.move.line'].search(
            ['|', ('result_package_id', '=', self.id), ('package_id', '=', self.id)],
            order='date desc, id desc',
            limit=1,
        )
        return move_line.picking_id
