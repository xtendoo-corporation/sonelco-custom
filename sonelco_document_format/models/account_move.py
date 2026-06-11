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
        """Prepare invoice lines grouped by pickings."""
        self.ensure_one()

        picking_dict = OrderedDict()
        lines_dict = OrderedDict()

        print("\n" + "=" * 80)
        print("DEBUG lines_grouped_by_picking", self.name)
        print("=" * 80)

        sign = (
            -1.0
            if self.move_type == "out_refund"
               and (
                   not self.reversed_entry_id
                   or self.reversed_entry_id.picking_ids != self.picking_ids
               )
            else 1.0
        )

        so_dict = {
            picking.sale_id: picking
            for picking in self.picking_ids
            if picking.sale_id
        }

        # secciones / notas
        for line in self.invoice_line_ids.filtered(
            lambda x: x.display_type in ("line_section", "line_note")
        ):
            lines_dict.setdefault(line, 0)

        # productos
        for line in self.invoice_line_ids.filtered(
            lambda x: x.display_type == "product"
        ):

            print("\nLINEA:")
            print(" name:", line.name)
            print(" product:", line.product_id.name)
            print(" type:", line.product_id.type)
            print(" qty:", line.quantity)
            print(" moves:", line.move_line_ids.ids)
            print(" sale:", line.sale_line_ids.ids)

            remaining_qty = line.quantity
            found_picking = False

            # productos con stock
            for move in line.move_line_ids:

                print(
                    " MOVE",
                    move.id,
                    "picking",
                    move.picking_id.name if move.picking_id else None
                )

                if not move.picking_id:
                    continue

                found_picking = True

                key = (move.picking_id, line)

                picking_dict.setdefault(key, 0)

                qty = self._get_signed_quantity_done(
                    line,
                    move,
                    sign
                )

                picking_dict[key] += qty
                remaining_qty -= qty

            # servicios / sin movimientos
            if not line.move_line_ids:
                print(
                    " SIN MOVES -> NO PICKING:",
                    line.product_id.name
                )

                lines_dict[line] = line.quantity

                continue

            # resto pendiente
            if not float_is_zero(
                remaining_qty,
                precision_rounding=line.product_id.uom_id.rounding or 0.01,
            ):
                print(
                    " RESTANTE:",
                    line.product_id.name,
                    remaining_qty
                )

                lines_dict[line] = remaining_qty

        print("\n" + "*" * 50)
        print("PICKING_DICT")
        for k, v in picking_dict.items():
            print(
                k[0].name,
                k[1].product_id.name,
                v
            )

        print("LINES_DICT")
        for k, v in lines_dict.items():
            print(
                k.product_id.name,
                v
            )

        print("*" * 50)

        no_picking = [
            {
                "picking": False,
                "line": key,
                "quantity": value,
            }
            for key, value in lines_dict.items()
        ]

        with_picking = [
            {
                "picking": key[0],
                "line": key[1],
                "quantity": value,
            }
            for key, value in picking_dict.items()
        ]

        print("NO PICKING FINAL:", no_picking)
        print("WITH PICKING FINAL:", with_picking)

        return (
            self._sort_grouped_lines(with_picking)
            + self._sort_grouped_lines(no_picking)
        )

    @api.onchange("ref")
    def _onchange_ref(self):
        self.facturae_receiver_contract_reference = self.ref

    def _l10n_es_facturae_sign_xml(self, edi_data, signature_data):
        """Override to replace single quotes with double quotes in XML declaration."""
        result = super()._l10n_es_facturae_sign_xml(edi_data, signature_data)
        if isinstance(result, bytes):
            result = result.replace(
                b"<?xml version='1.0' encoding='UTF-8'?>",
                b'<?xml version="1.0" encoding="UTF-8"?>',
            )
        return result


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def _get_price_total_and_subtotal_model(
        self,
        price_unit,
        quantity,
        discount,
        currency,
        product,
        partner,
        taxes,
        move_type,
    ):
        """This method is used to compute 'price_total' & 'price_subtotal'.

        :param price_unit:  The current price unit.
        :param quantity:    The current quantity.
        :param discount:    The current discount.
        :param currency:    The line's currency.
        :param product:     The line's product.
        :param partner:     The line's partner.
        :param taxes:       The applied taxes.
        :param move_type:   The type of the move.
        :return:            A dictionary containing 'price_subtotal' & 'price_total'.
        """
        res = {}

        # Compute 'price_subtotal'.
        line_discount_price_unit = price_unit * (1 - (discount / 100.0))
        subtotal = quantity * line_discount_price_unit

        # Compute 'price_total'.
        if taxes:
            taxes_res = taxes._origin.with_context(force_sign=1).compute_all(
                line_discount_price_unit,
                quantity=quantity,
                currency=currency,
                product=product,
                partner=partner,
                is_refund=move_type in ("out_refund", "in_refund"),
            )
            res["price_subtotal"] = taxes_res["total_excluded"]
            res["price_total"] = taxes_res["total_included"]
        else:
            res["price_total"] = res["price_subtotal"] = subtotal
        # In case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
        return res
