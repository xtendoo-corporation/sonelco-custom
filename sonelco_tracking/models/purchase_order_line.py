from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount_display = fields.Float(
        string="Descuento %",
        compute="_compute_discount_display",
        store=False
    )

    @api.depends('discount')
    def _compute_discount_display(self):
        for line in self:
            line.discount_display = line.discount
