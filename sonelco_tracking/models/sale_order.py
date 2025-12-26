from datetime import datetime, timedelta

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    type_id = fields.Many2one(
        comodel_name="sale.order.type",
        string="Type",
        compute="_compute_sale_type_id",
        precompute=True,
        store=True,
        readonly=False,
        ondelete="restrict",
        copy=True,
        check_company=True,
        tracking=True,
    )
