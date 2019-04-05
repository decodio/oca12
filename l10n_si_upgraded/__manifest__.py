# -*- coding: utf-8 -*-
# Copyright 2018 Mentis d.o.o.
# Copyright 2018 Luxim d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Slovenian Accounting and Taxes",
    "summary": "Slovenian account chart, taxes and fiscal forms",
    "version": "10.0.1.0.0",
    "license": 'AGPL-3',
    "author": "Mentis d.o.o., "
              "Luxim d.o.o., "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-slovenia",
    "category": "Localization/Account Charts",
    "depends": [
        "account",
        "base_iban",
        "base_vat",
        "account_cancel"
    ],
    "data": [
        "data/l10n_si_chart_data.xml",
        "data/account.account.template.csv",
        "data/account.chart.template.csv",
        "data/account.account.tag.csv",
        "data/account.tax.template.csv",
        "data/account.fiscal.position.template.csv",
        "data/account.fiscal.position.account.template.csv",
        "data/account.fiscal.position.tax.template.csv",
        "data/res.bank.xml",
        # "data/account_chart_template_data.yml"
    ],
    'auto_install': False,
    "installable": True,
}
