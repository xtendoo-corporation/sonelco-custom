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
            if res['price'] != 0:
                res['price'] = self.fixed_price
        return res

class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    def _get_shipment_rate(self):
        vals = self.carrier_id.rate_shipment(self.order_id)
        if vals.get('success'):
            if "Portes" in self.carrier_id.name:
                if vals['price'] != 0:
                    self.delivery_message = vals.get('warning_message', False)
                    self.delivery_price = self.carrier_id.fixed_price
                    self.display_price = self.carrier_id.fixed_price
                    return {}
                else:
                    self.delivery_message = vals.get('warning_message', False)
                    self.delivery_price = 0.0
                    self.display_price = 0.0
                    return {}
            self.delivery_message = vals.get('warning_message', False)
            self.delivery_price = vals['price']
            self.display_price = vals['carrier_price']
            return {}
        return {'error_message': vals['error_message']}
