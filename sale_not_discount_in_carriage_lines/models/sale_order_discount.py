from odoo import models

class SaleOrderDiscountInherit(models.TransientModel):
    _inherit = 'sale.order.discount'

    def action_apply_discount(self):
        self.ensure_one()
        self = self.with_company(self.company_id)
        categoria_excluir = self.env['product.category'].search([('name', '=', 'Transportes')], limit=1)
        if categoria_excluir:
            lineas_filtradas = self.sale_order_id.order_line.filtered(
                lambda l: l.product_id.categ_id != categoria_excluir
            )
            lineas_filtradas.write({'discount': self.discount_percentage * 100})
        else:
            self._create_discount_lines()
