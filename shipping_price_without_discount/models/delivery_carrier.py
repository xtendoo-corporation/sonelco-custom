# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import psycopg2

from odoo import api, fields, models, registry, SUPERUSER_ID, _

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    def rate_shipment(self, order):
        res = super(DeliveryCarrier, self).rate_shipment(order)
        if "Portes" in self.name:
            res['price'] = self.fixed_price
        return res

class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    def _get_shipment_rate(self):
        res = super(ChooseDeliveryCarrier, self)._get_shipment_rate()
        if "Portes" in self.carrier_id.name:
            self.display_price = self.carrier_id.fixed_price
        return res
