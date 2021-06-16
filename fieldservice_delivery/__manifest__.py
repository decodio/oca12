# Copyright (C) 2018, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Field Service - Delivery',
    'summary': 'Select delivery methods and carriers on Field Service orders',
    'version': '12.0.2.0.0',
    'category': 'Field Service',
    'author': "Open Source Integrators, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/field-service',
    'depends': [
        'fieldservice_stock_request',
        'delivery',
    ],
    'data': [
        'views/fsm_order.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'AGPL-3',
    'development_status': 'Beta',
    'maintainers': [
        'max3903',
    ],
}
