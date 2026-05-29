from odoo import fields, models


class StockQuantPackage(models.Model):
    _inherit = 'mrp.bom.line'

    location_plane = fields.Char('Localizacion')

