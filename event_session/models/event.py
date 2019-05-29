# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EventEvent(models.Model):
    _inherit = 'event.event'

    session_ids = fields.One2many(
        comodel_name='event.session',
        inverse_name='event_id',
        string='Sessions',
    )
    sessions_count = fields.Integer(
        compute='_compute_sessions_count',
        string='Total event sessions',
        store=True,
    )
    seats_available_expected = fields.Integer(
        compute='_compute_seats_available_expected',
        string='Available expected seats',
        readonly=True,
        store=True,
    )
    draft_state = fields.Integer(
        compute='_compute_state_numbers',
        string=' # No of Draft Registrations',
        store=True,
    )
    cancel_state = fields.Integer(
        compute='_compute_state_numbers',
        string=' # No of Cancelled Registrations',
        store=True,
    )
    confirm_state = fields.Integer(
        compute='_compute_state_numbers',
        string=' # No of Confirmed Registrations',
        store=True,
    )

    @api.multi
    @api.depends('session_ids')
    def _compute_sessions_count(self):
        for event in self:
            event.sessions_count = len(event.session_ids)

    @api.multi
    @api.constrains('seats_max', 'seats_available')
    def _check_seats_limit(self):
        for event in self:
            if not event.session_ids:
                return super(EventEvent, event)._check_seats_limit()

    @api.multi
    @api.depends('seats_max', 'seats_expected')
    def _compute_seats_available_expected(self):
        for this in self:
            seats = this.seats_max - this.seats_expected
            this.seats_available_expected = seats

    @api.multi
    @api.depends('registration_ids.state')
    def _compute_state_numbers(self):
        for this in self:
            this.draft_state = len(this.registration_ids.filtered(
                lambda x: x.state == 'draft'
            ))
            this.cancel_state = len(this.registration_ids.filtered(
                lambda x: x.state == 'cancel'
            ))
            this.confirm_state = len(this.registration_ids.filtered(
                lambda x: x.state == 'confirm'
            ))


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    event_sessions_count = fields.Integer(
        related='event_id.sessions_count',
        readonly=True,
    )
    session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
        ondelete='restrict',
    )

    @api.multi
    @api.constrains('event_id', 'session_id', 'state')
    def _check_seats_limit(self):
        for registration in self.filtered('session_id'):
            if (registration.session_id.seats_availability == 'limited' and
                    registration.session_id.seats_available < 1 and
                    registration.state == 'open'):
                raise ValidationError(
                    _('No more seats available for this event.'))

    @api.multi
    def confirm_registration(self):
        for reg in self:
            if not reg.event_id.session_ids:
                super(EventRegistration, reg).confirm_registration()
            reg.state = 'open'
            onsubscribe_schedulers = \
                reg.session_id.event_mail_ids.filtered(
                    lambda s: s.interval_type == 'after_sub')
            onsubscribe_schedulers.execute()
