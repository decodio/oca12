# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# Copyright 2020 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'JIRA Connector Tempo: Project Roles',
    'version': '12.0.1.1.0',
    'category': 'Connector',
    'website': 'https://github.com/OCA/connector-jira',
    'author':
        'CorporateHub, '
        'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'summary': 'Provide Assigments to Tempo and import Roles from Worklogs',
    'depends': [
        'connector_jira_tempo_base',
        'project_role',
        'hr_timesheet_role',
    ],
    'data': [
        'views/jira_backend.xml',
    ],
}
