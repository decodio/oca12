# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo https://www.escodoo.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class FleetVehicleInspection(models.Model):

    _name = 'fleet.vehicle.inspection'
    _description = 'Fleet Vehicle Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    READONLY_STATES = {
        'confirmed': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    name = fields.Char(
        'Reference',
        required=True,
        index=True,
        copy=False,
        default='New'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ], string='Status',
        copy=False, index=True, readonly=True, track_visibility='onchange',
        default='draft',
        help=" * Draft: not confirmed yet.\n"
             " * Confirmed: inspection has been confirmed.\n"
             " * Cancelled: has been cancelled, can't be confirmed anymore.")

    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        'Vehicle',
        help='Fleet Vehicle',
        track_visibility="onchange",
        required=True,
        states=READONLY_STATES
    )

    driver_id = fields.Many2one(
        'res.partner',
        'Driver',
        track_visibility="onchange",
        help='Driver of the vehicle'
    )

    odometer_id = fields.Many2one(
        'fleet.vehicle.odometer',
        'Odometer',
        help='Odometer measure of the vehicle at the moment of this log'
    )

    odometer = fields.Float(
        compute="_compute_odometer",
        inverse='_inverse_odometer',
        string='Last Odometer',
        help='Odometer measure of the vehicle at the moment of this log',
        track_visibility="onchange",
        stored=True,
        states=READONLY_STATES,
    )

    odometer_unit = fields.Selection([
        ('kilometers', 'Kilometers'),
        ('miles', 'Miles')
    ], 'Odometer Unit', default='kilometers',
        required=True,
        readonly=True,
    )

    date_inspected = fields.Datetime(
        'Inspection Date',
        required=True,
        default=fields.Datetime.now,
        help='Date when the vehicle has been inspected',
        track_visibility="onchange",
        copy=False,
        states=READONLY_STATES,
    )

    inspected_by = fields.Many2one(
        'res.partner',
        'Inspected By',
        track_visibility="onchange",
        states=READONLY_STATES,
    )

    direction = fields.Selection(
        selection=[('in', 'IN'),
                   ('out', 'OUT')],
        default='out',
        states=READONLY_STATES,
    )

    note = fields.Html('Notes', states=READONLY_STATES)

    inspection_line_ids = fields.One2many(
        'fleet.vehicle.inspection.line',
        'inspection_id',
        string='Inspection Lines',
        copy=True,
        auto_join=True,
        states=READONLY_STATES,
    )

    result = fields.Selection([
        ('todo', 'Todo'),
        ('success', 'Success'),
        ('failure', 'Failure')
    ], 'Inspection Result',
        default='todo',
        compute="_compute_inspection_result",
        readonly=True,
        copy=False,
        store=True,
    )

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.driver_id = self.vehicle_id.driver_id
            self.odometer_unit = self.vehicle_id.odometer_unit

    @api.depends('inspection_line_ids', 'state')
    def _compute_inspection_result(self):
        for rec in self:
            if rec.inspection_line_ids:
                if any(line.result == "todo" for line in rec.inspection_line_ids):
                    rec.result = "todo"
                elif any(line.result == "failure" for line in rec.inspection_line_ids):
                    rec.result = "failure"
                else:
                    rec.result = "success"
            else:
                rec.result = "todo"

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            if vals.get('direction') == 'out':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'fleet.vehicle.inspection.out') or '/'
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'fleet.vehicle.inspection.in') or '/'
        return super(FleetVehicleInspection, self).create(vals)

    @api.multi
    def button_cancel(self):
        records = self.filtered(lambda rec: rec.state in ["draft", "confirmed"])
        return records.write({"state": "cancel"})

    @api.multi
    def button_confirm(self):
        if any(not rec.odometer for rec in self):
            raise UserError(
                _("Emptying the odometer value of a " "vehicle is not allowed.")
            )
        if any(not rec.inspection_line_ids for rec in self) or any(
            line.result == "todo" for line in self.mapped("inspection_line_ids")
        ):
            raise UserError(
                _("Inspection cannot be completed. " "There are uninspected items.")
            )
        if any(rec.state not in ["draft", "cancel"] for rec in self):
            raise ValidationError(
                _("Only inspections in 'draft' or 'cancel' states can be confirmed")
            )
        return self.write({"state": "confirmed"})

    @api.multi
    def button_draft(self):
        return self.write({"state": "draft", "result": "todo"})

    def _compute_odometer(self):
        for rec in self:
            rec.odometer = False
            if rec.odometer_id:
                rec.odometer = rec.odometer_id.value

    def _inverse_odometer(self):
        for rec in self:
            if rec.odometer:
                odometer = self.env["fleet.vehicle.odometer"].create(
                    {
                        "value": rec.odometer,
                        "date": rec.date_inspected or fields.Date.context_today(rec),
                        "vehicle_id": rec.vehicle_id.id,
                    }
                )
                self.odometer_id = odometer
