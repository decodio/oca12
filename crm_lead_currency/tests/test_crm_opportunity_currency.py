# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import SavepointCase


class TestCrmOpportunityCurrency(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lead = cls.env['crm.lead'].create({
            'name': 'test lead'
        })

    def test_is_same_currency(self):
        self.lead.customer_currency_id = self.lead.company_id.currency_id
        self.assertTrue(self.lead.is_same_currency)
        self.lead.customer_currency_id = self.ref('base.CHF')
        self.assertFalse(self.lead.is_same_currency)

    def test_same_currency_planned_revenue_not_updated(self):
        self.lead.customer_currency_id = self.lead.company_id.currency_id
        self.lead.planned_revenue = 100
        self.lead.amount_customer_currency = 124
        self.lead._onchange_currency()
        self.assertEqual(self.lead.planned_revenue, 100)

    def test_different_currency_planned_revenue_updated(self):
        self.lead.planned_revenue = 100
        self.lead.customer_currency_id = self.ref('base.CHF')
        self.lead.amount_customer_currency = 124
        self.lead._onchange_currency()
        self.assertNotEqual(self.lead.planned_revenue, 100)
