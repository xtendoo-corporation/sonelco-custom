from odoo import models, fields, api, _
from odoo.exceptions import UserError



class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    delivery_ids = fields.Many2one(
        comodel_name='stock.picking', string='Delivery',
        compute="_compute_delivery_ids",
        default=lambda self: self._get_delivery_ids(),
        store=True,


    )

    def _compute_delivery_ids(self):
        delivery_ids = False
        domain = ['|', ('result_package_id', 'in', self.ids), ('package_id', 'in', self.ids)]
        move_line = self.env['stock.move.line'].search(domain)
        if move_line:
            delivery_ids = self.env['stock.picking'].search(
                [('id', '=', move_line[0].picking_id.id)], limit=1)
        self.delivery_ids = delivery_ids

    def _get_delivery_ids(self):
        delivery_ids = False
        domain = ['|', ('result_package_id', 'in', self.ids), ('package_id', 'in', self.ids)]
        move_line = self.env['stock.move.line'].search(domain)
        if move_line:
            delivery_ids = self.env['stock.picking'].search(
                [('id', '=', move_line[0].picking_id.id)], limit=1)
        return delivery_ids
