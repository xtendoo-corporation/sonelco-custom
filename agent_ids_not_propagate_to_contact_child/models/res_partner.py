
from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _commercial_fields(self):
        res = super(ResPartner, self)._commercial_fields()
        if 'agent_ids' in res:
            res.remove('agent_ids')
        return res
