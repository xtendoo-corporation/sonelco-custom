from odoo import models, fields, api, _


class StockQuantPackage(models.Model):
    _inherit = 'mrp.bom.line'

    location_plane = fields.Char('Localización')

