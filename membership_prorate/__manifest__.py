# Copyright 2015 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Prorate membership fee',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Association',
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/vertical-association',
    'depends': [
        'membership',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
}
