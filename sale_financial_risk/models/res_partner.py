# Copyright 2016-2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    risk_sale_order_include = fields.Boolean(
        string='Include Sales Orders', help='Full risk computation')
    risk_sale_order_limit = fields.Monetary(
        string='Limit Sales Orders',
        currency_field="risk_currency_id",
        help='Set 0 if it is not locked')
    risk_sale_order = fields.Monetary(
        compute='_compute_risk_sale_order',
        currency_field="risk_currency_id",
        compute_sudo=True,
        string='Total Sales Orders Not Invoiced',
        help='Total not invoiced of sales orders in Sale Order state')

    def _get_risk_sale_order_domain(self):
        # When p is NewId object instance bool(p.id) is False
        commercial_partners = self.filtered(lambda p: (
            p.customer and p.id and p == p.commercial_partner_id
        ))
        risk_states = self.env['sale.order']._get_risk_states()
        return self._get_risk_company_domain() + [
            ('state', 'in', risk_states),
            ('commercial_partner_id', 'in', commercial_partners.ids),
        ]

    @api.depends('sale_order_ids.order_line.risk_amount',
                 'child_ids.sale_order_ids.order_line.risk_amount')
    def _compute_risk_sale_order(self):
        self.update({'risk_sale_order': 0.0})
        orders_group = self.env['sale.order.line'].read_group(
            domain=self._get_risk_sale_order_domain(),
            fields=['commercial_partner_id', 'company_id', 'risk_amount'],
            groupby=['commercial_partner_id', 'company_id'],
            orderby='id',
            lazy=False,
        )
        for group in orders_group:
            partner = self.browse(
                group["commercial_partner_id"][0], self._prefetch)
            company = self.env['res.company'].browse(
                group['company_id'][0] or self.env.user.company_id.id
            )
            company_currency = company.currency_id
            partner.risk_sale_order = company_currency._convert(
                group["risk_amount"], partner.risk_currency_id,
                company, fields.Date.context_today(self),
                round=False)

    @api.model
    def _risk_field_list(self):
        res = super(ResPartner, self)._risk_field_list()
        res.append(('risk_sale_order', 'risk_sale_order_limit',
                    'risk_sale_order_include'))
        return res

    def _get_field_risk_model_domain(self, field_name):
        if field_name == 'risk_sale_order':
            return 'sale.order.line', self._get_risk_sale_order_domain()
        else:
            return super()._get_field_risk_model_domain(field_name)
