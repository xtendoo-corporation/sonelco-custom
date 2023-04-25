

from odoo import api, models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    link = fields.Char(string='Link')
