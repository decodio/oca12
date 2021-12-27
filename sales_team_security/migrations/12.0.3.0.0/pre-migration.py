# Copyright 2021 Tecnativa - Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """Adjust record rules according new definition."""
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    record = env.ref("sales_team_security.sales_team_team_rule", False)
    if record:
        record.groups = [
            (3, env.ref("sales_team_security.group_sale_team_manager").id),
            (4, env.ref("sales_team.group_sale_salesman").id),
        ]
    record = env.ref("sales_team_security.sale_order_team_rule", False)
    if record:
        record.domain_force = (
            "['|', ('user_id','=',user.id), ('user_id','=',False), '|', "
            "('team_id', '=', user.sale_team_id.id), ('team_id', '=', False)]"
        )
    record = env.ref("sales_team_security.sale_order_report_team_rule", False)
    if record:
        record.domain_force = (
            "['|', ('user_id','=',user.id), ('user_id','=',False), '|', "
            "('team_id', '=', user.sale_team_id.id), ('team_id', '=', False)]"
        )
    record = env.ref("sales_team_security.sale_order_line_team_rule", False)
    if record:
        record.domain_force = (
            "['|', '|', ('salesman_id', '=', user.id), "
            "('salesman_id', '=', False), '|', "
            "('order_id.team_id', '=', user.sale_team_id.id), "
            "('order_id.team_id', '=', False)]"
        )
    record = env.ref("sales_team_security.crm_lead_team_rule", False)
    if record:
        record.domain_force = (
            "['|', ('user_id','=',user.id), ('user_id','=',False), '|', "
            "('team_id', '=', user.sale_team_id.id), ('team_id', '=', False)]"
        )
    record = env.ref("sales_team_security.crm_activity_report_team", False)
    if record:
        record.domain_force = (
            "['|', ('user_id','=',user.id), ('user_id','=',False), '|', "
            "('team_id', '=', user.sale_team_id.id), ('team_id', '=', False)]"
        )
