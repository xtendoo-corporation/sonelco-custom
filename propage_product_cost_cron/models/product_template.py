# Copyright 2024 Salvador González Jiménez - Xtendoo
from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def cron_update_bom_costs(self):
        templates = self.search([('bom_count', '>', 0)])

        if templates:
            templates.mapped('product_variant_id').action_bom_cost()
