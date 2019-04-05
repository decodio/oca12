# Copyright 2018 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_timesheet_role_required = fields.Boolean(
        string='Timesheet Role Required',
        default=lambda self: self._default_is_timesheet_role_required(),
    )
    limit_timesheet_role_to_assignments = fields.Boolean(
        string='Limit Timesheet Role to Assignments',
        default=(
            lambda self: self._default_limit_timesheet_role_to_assignments()
        ),
    )

    @api.model
    def _default_is_timesheet_role_required(self):
        company = self.env['res.company'].browse(
            self._context.get('company_id', self.env.user.company_id.id)
        )
        return company.is_timesheet_role_required

    @api.model
    def _default_limit_timesheet_role_to_assignments(self):
        company = self.env['res.company'].browse(
            self._context.get('company_id', self.env.user.company_id.id)
        )
        return company.limit_timesheet_role_to_assignments

    @api.model
    def create(self, values):
        company = None
        if 'company_id' in values:
            company = self.env['res.company'].browse(values['company_id'])

        if company and 'is_timesheet_role_required' not in values:
            values['is_timesheet_role_required'] = (
                company.is_timesheet_role_required
            )

        if company and 'limit_timesheet_role_to_assignments' not in values:
            values['limit_timesheet_role_to_assignments'] = (
                company.limit_timesheet_role_to_assignments
            )

        return super().create(values)
