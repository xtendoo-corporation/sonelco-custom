from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order"

    @api.onchange('pricelist_id')
    def _recalculate_lines(self):
        for line in self.order_line:
            if line.pricelist_id == self.pricelist_id:
                return
            line.pricelist_id = self.pricelist_id
            if line.pricelist_id.discount_policy == 'without_discount':
                pricelist_item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', line.pricelist_id.id),
                ])
                line.price_unit = line.product_id.lst_price
                line.discount = pricelist_item.percent_price

            if line.pricelist_id.discount_policy == 'with_discount':
                line.discount = 0.0
                line.price_unit = line.product_id.with_context(pricelist=line.order_id.pricelist_id.id, uom=line.product_uom.id).price
