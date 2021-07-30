# Copyright 2015 Tecnativa - Pedro M. Baeza
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo import fields
from datetime import date


class TestMembershipVariablePeriod(common.TransactionCase):

    def setUp(self):
        super(TestMembershipVariablePeriod, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Membership product with variable period',
            'membership': True,
            'membership_date_from': '2015-01-01',
            'membership_date_to': '2015-12-31',
            'membership_type': 'variable',
            'membership_interval_qty': 1,
            'membership_interval_unit': 'weeks',
        })
        self.partner = self.env['res.partner'].create({'name': 'Test'})

    def test_create_invoice_membership_product_days(self):
        self.product.membership_interval_unit = 'days'
        self.product.membership_interval_qty = 20
        account = self.partner.property_account_receivable_id.id
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'date_invoice': '2015-07-01',
            'account_id': account,
        })
        self.env['account.invoice.line'].create({
            'account_id': account,
            'product_id': self.product.id,
            'price_unit': self.product.list_price,
            'name': 'Membership w/o prorrate',
            'invoice_id': invoice.id,
            'quantity': 1.0,
        })
        membership_line = invoice.invoice_line_ids[0].membership_lines[0]
        membership_line.write({'state': 'invoiced'})
        self.assertEqual(membership_line.date_from,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(membership_line.date_to,
                         fields.Date.from_string('2015-07-20'))
        self.assertEqual(self.partner.membership_start,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(self.partner.membership_stop,
                         fields.Date.from_string('2015-07-20'))

    def test_create_invoice_membership_product_week(self):
        account = self.partner.property_account_receivable_id.id
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'date_invoice': '2015-07-01',
            'account_id': account,
        })
        self.env['account.invoice.line'].create({
            'account_id': account,
            'product_id': self.product.id,
            'price_unit': self.product.list_price,
            'name': 'Membership w/o prorrate',
            'invoice_id': invoice.id,
            'quantity': 1.0,
        })
        membership_line = invoice.invoice_line_ids[0].membership_lines[0]
        membership_line.write({'state': 'invoiced'})
        self.assertEqual(membership_line.date_from,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(membership_line.date_to,
                         fields.Date.from_string('2015-07-07'))
        self.assertEqual(self.partner.membership_start,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(self.partner.membership_stop,
                         fields.Date.from_string('2015-07-07'))

    def test_create_invoice_membership_product_month(self):
        self.product.membership_interval_unit = 'months'
        account = self.partner.property_account_receivable_id.id
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'date_invoice': '2015-04-15',
            'account_id': account,
        })
        self.env['account.invoice.line'].create({
            'account_id': account,
            'product_id': self.product.id,
            'price_unit': self.product.list_price,
            'name': 'Membership with prorrate',
            'invoice_id': invoice.id,
            'quantity': 1.0,
        })
        membership_line = invoice.invoice_line_ids[0].membership_lines[0]
        membership_line.write({'state': 'invoiced'})
        self.assertEqual(membership_line.date_from,
                         fields.Date.from_string('2015-04-15'))
        self.assertEqual(membership_line.date_to,
                         fields.Date.from_string('2015-05-14'))
        self.assertEqual(self.partner.membership_start,
                         fields.Date.from_string('2015-04-15'))
        self.assertEqual(self.partner.membership_stop,
                         fields.Date.from_string('2015-05-14'))

    def test_create_invoice_membership_product_year(self):
        self.product.membership_interval_unit = 'years'
        account = self.partner.property_account_receivable_id.id
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'date_invoice': '2016-07-01',  # It's leap year
            'account_id': account,
        })
        self.env['account.invoice.line'].create({
            'account_id': account,
            'product_id': self.product.id,
            'price_unit': self.product.list_price,
            'name': 'Membership with prorrate',
            'invoice_id': invoice.id,
            'quantity': 1.0,
        })
        membership_line = invoice.invoice_line_ids[0].membership_lines[0]
        membership_line.write({'state': 'invoiced'})
        self.assertEqual(membership_line.date_from,
                         fields.Date.from_string('2016-07-01'))
        self.assertEqual(membership_line.date_to,
                         fields.Date.from_string('2017-06-30'))
        self.assertEqual(self.partner.membership_start,
                         fields.Date.from_string('2016-07-01'))
        self.assertEqual(self.partner.membership_stop,
                         fields.Date.from_string('2017-06-30'))

    def test_create_invoice_membership_product_year_several(self):
        self.product.membership_interval_unit = 'years'
        account = self.partner.property_account_receivable_id.id
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'date_invoice': '2015-07-01',
            'account_id': account,
        })
        self.env['account.invoice.line'].create({
            'account_id': account,
            'product_id': self.product.id,
            'price_unit': self.product.list_price,
            'name': 'Membership with prorrate',
            'invoice_id': invoice.id,
            'quantity': 3.0,
        })
        membership_lines = invoice.invoice_line_ids[0].membership_lines
        membership_lines.write({'state': 'invoiced'})
        self.assertEqual(len(membership_lines), 1)
        self.assertEqual(membership_lines[0].date_from,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(membership_lines[0].date_to,
                         fields.Date.from_string('2018-06-30'))
        self.assertEqual(self.partner.membership_start,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(self.partner.membership_stop,
                         fields.Date.from_string('2018-06-30'))

    def test_modify_invoice_membership_product(self):
        self.product.membership_interval_unit = 'years'
        account = self.partner.property_account_receivable_id.id
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'date_invoice': '2015-07-01',
            'account_id': account,
        })
        self.env['account.invoice.line'].create({
            'account_id': account,
            'product_id': self.product.id,
            'price_unit': self.product.list_price,
            'name': 'Membership w/o prorrate',
            'invoice_id': invoice.id,
            'quantity': 1.0,
        })
        invoice.invoice_line_ids[0].quantity = 2.0
        membership_lines = invoice.invoice_line_ids[0].membership_lines
        membership_lines.write({'state': 'invoiced'})
        self.assertEqual(len(membership_lines), 1)
        self.assertEqual(membership_lines[0].date_from,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(membership_lines[0].date_to,
                         fields.Date.from_string('2017-06-30'))
        self.assertEqual(self.partner.membership_start,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(self.partner.membership_stop,
                         fields.Date.from_string('2017-06-30'))
        # Remove quantity
        invoice.invoice_line_ids[0].quantity = 1.0
        membership_lines = invoice.invoice_line_ids[0].membership_lines
        self.assertEqual(len(membership_lines), 1)
        self.assertEqual(membership_lines[0].date_from,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(membership_lines[0].date_to,
                         fields.Date.from_string('2016-06-30'))

    def test_modify_invoice_membership_product_type(self):
        self.product.membership = False
        account = self.partner.property_account_receivable_id.id
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'date_invoice': '2015-07-01',
            'account_id': account,
        })
        self.env['account.invoice.line'].create({
            'account_id': account,
            'product_id': self.product.id,
            'price_unit': self.product.list_price,
            'name': 'Membership w/o prorrate',
            'invoice_id': invoice.id,
            'quantity': 1.0,
        })
        self.assertFalse(invoice.invoice_line_ids[0].membership_lines)
        self.product.membership = True
        invoice.invoice_line_ids[0].quantity = 1.0
        self.assertEqual(len(invoice.invoice_line_ids[0].membership_lines), 1)

    def test_create_and_modify_invoice_line_membership_product(self):
        account = self.partner.property_account_receivable_id.id
        self.product.membership_interval_qty = 20
        self.product.membership_interval_unit = 'days'
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'date_invoice': '2015-07-01',
            'account_id': account,
        })
        self.env['account.invoice.line'].create({
            'account_id': account,
            'product_id': self.product.id,
            'price_unit': self.product.list_price,
            'name': 'Membership w/o prorrate',
            'invoice_id': invoice.id,
            'quantity': 1.0,
        })
        membership_line = invoice.invoice_line_ids[0].membership_lines[0]
        membership_line.write({'state': 'invoiced'})
        self.assertEqual(membership_line.date_from,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(membership_line.date_to,
                         fields.Date.from_string('2015-07-20'))
        self.assertEqual(self.partner.membership_start,
                         fields.Date.from_string('2015-07-01'))
        self.assertEqual(self.partner.membership_stop,
                         fields.Date.from_string('2015-07-20'))

    def test_check_membership_expiry(self):
        self.env['membership.membership_line'].create({
            'partner': self.partner.id,
            'membership_id': self.product.id,
            'member_price': 1.0,
            'date': '2014-01-01',
            'date_from': '2014-01-01',
            'date_to': '2014-12-31',
            'state': 'paid',
        })
        # Force state to let the calculation return to the computed one
        free_state = self.partner.free_member
        self.partner.write({'free_member': not free_state})
        self.partner.write({'free_member': free_state})
        self.env['res.partner'].check_membership_expiry()
        self.assertEqual(self.partner.membership_state, 'old')

    def test_get_next_date(self):
        test_suite = [
            # Add here more border cases that can be detected in the future
            ('2015-01-01', "days", 25, date(day=26, month=1, year=2015)),
            ('2015-01-01', "weeks", 1, date(day=8, month=1, year=2015)),
            ('2015-01-01', "months", 3, date(day=1, month=4, year=2015)),
            ('2015-01-01', "years", 1, date(day=1, month=1, year=2016)),
        ]
        template_model = self.env['product.template']
        for old_date, interval, qty, next_date in test_suite:
            template = template_model.new()
            template.membership_type = 'variable'
            template.membership_interval_unit = interval
            template.membership_interval_qty = qty
            self.assertEqual(template._get_next_date(old_date), next_date)

    def test_create_invoice_line_with_no_product(self):
        account = self.partner.property_account_receivable_id.id
        invoice = self.env['account.invoice'].create({
            'partner_id': self.partner.id,
            'date_invoice': '2015-07-01',
            'account_id': account,
        })
        self.env['account.invoice.line'].create({
            'account_id': account,
            'price_unit': self.product.list_price,
            'name': 'No product',
            'invoice_id': invoice.id,
            'quantity': 1.0,
        })
        self.assertFalse(invoice.invoice_line_ids[0].product_id)
