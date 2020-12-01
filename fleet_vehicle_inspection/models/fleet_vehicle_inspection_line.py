# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo https://www.escodoo.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FleetVehicleInspectionLine(models.Model):

    _name = 'fleet.vehicle.inspection.line'
    _description = 'Fleet Vehicle Inspection Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    READONLY_STATES = {
        'confirmed': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    inspection_id = fields.Many2one(
        'fleet.vehicle.inspection',
        string='Inspection Reference',
        required=True,
        ondelete='cascade',
        index=True,
        copy=False)

    inspection_item_id = fields.Many2one(
        'fleet.vehicle.inspection.item',
        'Inspection Item',
        required=True,
        track_visibility="onchange",
        help='Inspection Item',
        states=READONLY_STATES,
    )

    result = fields.Selection([
        ('todo', 'Todo'),
        ('success', 'Success'),
        ('failure', 'Failure')
    ], 'Result', default='todo',
        help='Inspection Line Result ',
        readonly=True,
        required=True,
        copy=False
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ], related='inspection_id.state',
        string='Inspection Status',
        readonly=True,
        copy=False,
        store=True,
        default='draft'
    )

    @api.multi
    def action_item_success(self):
        return self.write({'result': 'success'})

    @api.multi
    def action_item_failure(self):
        return self.write({'result': 'failure'})
