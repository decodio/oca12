# Copyright 2015 Tecnativa - Pedro M. Baeza
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from datetime import timedelta
import math


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    def _prepare_membership_line(self, invoice, product, price_unit, line_id,
                                 qty=1.0):
        qty = int(math.ceil(qty))
        date_from = fields.Date.from_string(
            invoice.date_invoice or fields.Date.today())
        date_to = (product.product_tmpl_id._get_next_date(date_from, qty=qty) -
                   timedelta(days=1))
        return {
            'partner': invoice.partner_id.id,
            'membership_id': product.id,
            'member_price': price_unit,
            'date': invoice.date_invoice or fields.Date.today(),
            'date_from': fields.Date.to_string(date_from),
            'date_to': fields.Date.to_string(date_to),
            'state': 'waiting',
            'account_invoice_line': line_id,
        }

    @api.multi
    def write(self, vals):
        """Create before the lines of membership with variable period."""
        memb_line_model = self.env['membership.membership_line']
        if any(x in vals for x in ['product_id', 'quantity', 'invoice_id']):
            for line in self:
                product = (
                    self.env['product.product'].browse(vals['product_id']) if
                    vals.get('product_id') else line.product_id)
                invoice = (
                    self.env['account.invoice'].browse(vals['invoice_id']) if
                    vals.get('invoice_id') else line.invoice_id)
                if (invoice.type == 'out_invoice' and
                        product.membership and
                        product.membership_type == 'variable'):
                    quantity = float(vals.get('quantity', line.quantity))
                    price_unit = vals.get('price_unit', line.price_unit)
                    membership_vals = self._prepare_membership_line(
                        invoice, product, price_unit, line.id, qty=quantity)
                    if line.membership_lines:
                        if len(line.membership_lines) > 1:  # pragma: no cover
                            # Remove all except last one,
                            # only one membership line per invoice line
                            line.membership_lines[:-1].unlink()
                        # Update with changes
                        line.membership_lines[0].write(membership_vals)
                    else:
                        # Create membership line
                        memb_line_model.create(membership_vals)
        return super(AccountInvoiceLine, self).write(vals)

    @api.model
    def create(self, vals):
        price_unit = vals.get('price_unit', 0.0)
        line = super(AccountInvoiceLine, self).create(vals)
        if (line.invoice_id.type == 'out_invoice' and
                line.product_id.membership and
                line.product_id.membership_type == 'variable'):
            qty = float(line.quantity)
            membership_vals = self._prepare_membership_line(
                line.invoice_id, line.product_id, price_unit, line.id, qty=qty)
            # There's already the super line
            line.membership_lines[0].write(membership_vals)
        return line
