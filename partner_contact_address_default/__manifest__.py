# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Contact address default',
    'summary': 'Set a default delivery and invoice address for contacts',
    'version': '12.0.1.2.1',
    'development_status': 'Beta',
    'category': 'Generic Modules/Base',
    'website': 'https://github.com/OCA/partner-contact',
    'author': 'Tecnativa, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base_setup',
    ],
    'data': [
        'security/res_groups_security.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
}
