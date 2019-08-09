# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# Copyright 2015 Techrifiv Solutions Pte Ltd
# Copyright 2015 Statecraft Systems Pte Ltd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Currency Rate Inverted',
    'version': '12.0.1.0.0',
    'category': 'Accounting & Finance',
    'summary': 'Allows to maintain an exchange rate using the inversion '
               'method',
    'author': 'Eficent,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/currency',
    'license': 'AGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'views/res_currency_view.xml'
    ],
    "installable": True
}
