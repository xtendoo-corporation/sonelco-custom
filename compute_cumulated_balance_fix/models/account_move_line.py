# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, registry, SUPERUSER_ID, _
import re
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends_context('order_cumulated_balance', 'domain_cumulated_balance')
    def _compute_cumulated_balance(self):
        if not self.env.context.get('order_cumulated_balance'):
            # We do not come from search_read, so we are not in a list view, so it doesn't make any sense to compute the cumulated balance
            self.cumulated_balance = 0
            return

        # get the where clause
        query = self._where_calc(list(self.env.context.get('domain_cumulated_balance') or []))
        order_string = self._get_cumulated_balance_order(self._table, self.env.context.get('order_cumulated_balance'), query,
                                          reverse_direction=True)
        from_clause, where_clause, where_clause_params = query.get_sql()
        sql = """
               SELECT account_move_line.id, SUM(account_move_line.balance) OVER (
                   ORDER BY %(order_by)s
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
               )
               FROM %(from)s
               WHERE %(where)s
           """ % {'from': from_clause, 'where': where_clause or 'TRUE', 'order_by': order_string}
        self.env.cr.execute(sql, where_clause_params)
        result = {r[0]: r[1] for r in self.env.cr.fetchall()}
        for record in self:
            record.cumulated_balance = result[record.id]


    def _get_cumulated_balance_order( self, alias, order_spec, query, reverse_direction=False, seen=None):
        print("*" * 100)
        order_string = ", ".join(
            self._generate_order_by_inner(self._table, self.env.context.get('order_cumulated_balance'), query,
                                          reverse_direction=False))
        print("order_string ANTES", order_string)
        if '"account_move_line__move_id"."name"' in query:
            order_string = re.sub(r'("account_move_line"\."date") DESC', r'\1 ASC', order_string)
        else:
            order_string = re.sub(r'("account_move_line"\."date") DESC', r'\1 ASC', order_string)
        print("order_string DESPUES", order_string)
        return order_string



