# Copyright 2018 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.tools.misc import formatLang
from odoo.exceptions import ValidationError


class VatStatementIcpLine(models.Model):
    _name = 'l10n.nl.vat.statement.icp.line'
    _description = 'Intra-Community transactions (ICP) line'
    _order = 'partner_id, country_code'

    statement_id = fields.Many2one(
        'l10n.nl.vat.statement',
        'Statement',
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        readonly=True,
        required=True,
    )
    vat = fields.Char(
        string='VAT',
        readonly=True,
    )
    country_code = fields.Char(
        readonly=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        readonly=True
    )
    amount_products = fields.Monetary(readonly=True)
    format_amount_products = fields.Char(compute='_compute_icp_amount_format')
    amount_services = fields.Monetary(readonly=True)
    format_amount_services = fields.Char(compute='_compute_icp_amount_format')

    @api.depends('amount_products', 'amount_services')
    def _compute_icp_amount_format(self):
        for line in self:
            amount_products = formatLang(
                self.env, line.amount_products, monetary=True)
            amount_services = formatLang(
                self.env, line.amount_services, monetary=True)
            line.format_amount_products = amount_products
            line.format_amount_services = amount_services

    @api.constrains('country_code')
    def _check_country_code(self):
        europe_codes = self.env.ref('base.europe').country_ids.mapped('code')
        if "GB" not in europe_codes:
            # Allow GB lines from before the effective Brexit date
            brexit_date = fields.Date.from_string("2021-01-01")
            lines = self.filtered(
                lambda line: line.country_code != "GB" or
                line.statement_id.from_date >= brexit_date)
        else:
            lines = self
        country_codes = lines.mapped('country_code')
        if self.env.ref('base.nl').code in country_codes:
            raise ValidationError(_(
                'Wrong country code (NL) for ICP report.'))
        for code in country_codes:
            if code not in europe_codes:
                raise ValidationError(_(
                    'Wrong country code (%s) for ICP report. '
                    'Please check your configuration.') % code)
