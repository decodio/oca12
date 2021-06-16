# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
import odoo.addons.decimal_precision as dp


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    weight = fields.Float(digits=dp.get_precision('Stock Weight'))

    def _select(self):
        select_str = super()._select()
        select_str += """
            , sub.weight as weight
            """
        return select_str

    def _sub_select(self):
        select_str = super()._sub_select()
        select_str += """
            , SUM(
                pr.weight * invoice_type.sign_qty * ail.quantity / u.factor * u2.factor
            )
            AS weight
            """
        return select_str
