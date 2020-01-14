# Copyright 2017-2018 Tecnativa - Sergio Teruel
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, qty):
        vals = super()._prepare_invoice_line(qty)
        vals['purchase_price'] = self.purchase_price
        return vals
