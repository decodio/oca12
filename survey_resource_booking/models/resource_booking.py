# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.tests.common import Form
from odoo.tools.mail import email_split
from odoo.exceptions import UserError


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    survey_user_input_id = fields.Many2one(
        "survey.user_input",
        string="Survey user input",
        track_visibility="onchange",
        help="User responses to survey, as specified in the resource booking type.",
    )

    def action_invite_survey(self):
        """Invite requester to fill survey, if needed and possible."""
        for one in self:
            # Skip unconfirmed bookings, or finished user inputs
            if one.state != "confirmed":
                raise UserError(
                    _(
                        "Cannot invite to fill survey because booking not confirmed: %s"
                    )
                    % one.display_name
                )
            if one.survey_user_input_id.state == "done":
                raise UserError(
                    _(
                        "This booking's requester was already invited "
                        "to fill survey: %s"
                    )
                    % one.display_name
                )
            if not one.survey_user_input_id:
                if not one.type_id.survey_id:
                    raise UserError(
                        _("This booking's type has no survey defined: %s"),
                        one.display_name,
                    )
                if not email_split(one.partner_id.email):
                    raise UserError(
                        _(
                            "Cannot send survey invitation for this booking "
                            "because the requester has no email: %s"
                        )
                        % one.display_name
                    )
                one.survey_user_input_id = self.env[
                    "survey.user_input"
                ].create(
                    {
                        "partner_id": one.partner_id.id,
                        "survey_id": one.type_id.survey_id.id,
                        "type": "link",
                    }
                )
            # Enqueue survey invitation
            action = one.survey_user_input_id.action_survey_resend()
            wizard_f = Form(
                self.env[action["res_model"]].with_context(action["context"]),
            )
            wizard = wizard_f.save()
            wizard.send_mail()
