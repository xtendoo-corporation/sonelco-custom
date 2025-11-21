# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2018 Tecnativa - David Vidal
# Copyright 2018-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import api, models
from odoo.tools import float_is_zero


class AccountMove(models.Model):
    _inherit = "account.move"

    def lines_grouped_by_picking(self):
        """This prepares a data structure for printing the invoice report
        grouped by pickings."""
        self.ensure_one()
        picking_dict = OrderedDict()
        lines_dict = OrderedDict()
        # Not change sign if the credit note has been created from reverse move option
        # and it has the same pickings related than the reversed invoice instead of sale
        # order invoicing process after picking reverse transfer
        sign = (
            -1.0
            if self.move_type == "out_refund"
            and (
                not self.reversed_entry_id
                or self.reversed_entry_id.picking_ids != self.picking_ids
            )
            else 1.0
        )
        # Let's get first a correspondance between pickings and sales order
        so_dict = {x.sale_id: x for x in self.picking_ids if x.sale_id}
        # Now group by picking by direct link or via same SO as picking's one
        for line in self.invoice_line_ids.filtered(lambda x: x.display_type == 'line_section' or x.display_type == 'line_note'):
            key = line
            lines_dict.setdefault(key, 0)
        for line in self.invoice_line_ids.filtered(lambda x: x.display_type == 'product'):
            remaining_qty = line.quantity
            for move in line.move_line_ids:
                key = (move.picking_id, line)
                picking_dict.setdefault(key, 0)
                qty = self._get_signed_quantity_done(line, move, sign)
                picking_dict[key] += qty
                remaining_qty -= qty
            if not line.move_line_ids and line.sale_line_ids:
                for so_line in line.sale_line_ids:
                    if so_dict.get(so_line.order_id):
                        key = (so_dict[so_line.order_id], line)
                        picking_dict.setdefault(key, 0)
                        qty = so_line.product_uom_qty
                        picking_dict[key] += qty
                        remaining_qty -= qty
            if not float_is_zero(
                remaining_qty,
                precision_rounding=line.product_id.uom_id.rounding or 0.01,
            ):
                lines_dict[line] = remaining_qty
        no_picking = [
            {"picking": False, "line": key, "quantity": value}
            for key, value in lines_dict.items()
        ]
        with_picking = [
            {"picking": key[0], "line": key[1], "quantity": value}
            for key, value in picking_dict.items()
        ]
        return self._sort_grouped_lines(with_picking) + no_picking

    @api.onchange('ref')
    def _onchange_ref(self):
        self.facturae_receiver_contract_reference = self.ref

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes,
                                            move_type):
        ''' This method is used to compute 'price_total' & 'price_subtotal'.

        :param price_unit:  The current price unit.
        :param quantity:    The current quantity.
        :param discount:    The current discount.
        :param currency:    The line's currency.
        :param product:     The line's product.
        :param partner:     The line's partner.
        :param taxes:       The applied taxes.
        :param move_type:   The type of the move.
        :return:            A dictionary containing 'price_subtotal' & 'price_total'.
        '''
        res = {}

        # Compute 'price_subtotal'.
        line_discount_price_unit = price_unit * (1 - (discount / 100.0))
        subtotal = quantity * line_discount_price_unit

        # Compute 'price_total'.
        if taxes:
            taxes_res = taxes._origin.with_context(force_sign=1).compute_all(line_discount_price_unit,
                                                                             quantity=quantity, currency=currency,
                                                                             product=product, partner=partner,
                                                                             is_refund=move_type in ('out_refund',
                                                                                                     'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        # In case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
        return res
