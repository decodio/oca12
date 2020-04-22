# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# Copyright 2019 Dataplug (https://dataplug.io)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Online Bank Statements: PayPal.com',
    'version': '12.0.1.0.2',
    'author':
        'Brainbean Apps, '
        'Dataplug, '
        'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/bank-statement-import/',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'summary': 'Online bank statements for PayPal.com',
    'depends': [
        'account_bank_statement_import_online',
    ],
    'data': [
        'views/online_bank_statement_provider.xml',
    ],
    'installable': True,
}
