from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order"

    @api.onchange('pricelist_id')
    def _recalculate_lines(self):
        print("*"*50)
        print("_recalculate_lines")
        print("*"*50)
        self.action_update_prices()

    def action_update_prices(self):
        self.ensure_one()

        self._recompute_prices()

        # if self.pricelist_id:
        #     self.message_post(body=_(
        #         "Product prices have been recomputed according to pricelist %s.",
        #         self.pricelist_id._get_html_link(),
        #     ))
