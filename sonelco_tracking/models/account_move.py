from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    sale_type_id = fields.Many2one(
        comodel_name="sale.order.type",
        string="Sale Type",
        compute="_compute_sale_type_id",
        store=True,
        readonly=False,
        ondelete="restrict",
        copy=True,
        precompute=True,
        tracking=True,
    )
