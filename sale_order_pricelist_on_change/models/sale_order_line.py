from odoo import api, fields, models

import logging




class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _default_pricelist(self):
        return self.order_id.pricelist_id

    pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Pricelist',
        store=True,
        default=_default_pricelist,
    )

    @api.onchange('product_id')
    def product_id_change(self):
        result = super().product_id_change()
        self.pricelist_id = self.order_id.pricelist_id.id
        return result





