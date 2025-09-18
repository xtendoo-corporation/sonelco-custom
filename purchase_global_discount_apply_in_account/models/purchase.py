# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, registry, SUPERUSER_ID, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_invoice(self):
        res = super(PurchaseOrder, self)._prepare_invoice()
        if res.get('partner_id'):
            partner = self.env['res.partner'].browse(res['partner_id'])
            if partner.supplier_global_discount_ids:
                res['global_discount_ids'] = partner.supplier_global_discount_ids
        return res
