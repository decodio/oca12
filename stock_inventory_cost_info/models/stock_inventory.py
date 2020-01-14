# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    currency_id = fields.Many2one(
        string="Currency",
        related="inventory_id.company_id.currency_id",
        readonly=True,
    )
    adjustment_cost = fields.Monetary(
        string="Adjustment cost",
        compute="_compute_adjustment_cost",
        store=True,
    )

    @api.depends("product_qty", "theoretical_qty", "inventory_id.state")
    def _compute_adjustment_cost(self):
        for record in self:
            adjusted_qty = record.product_qty - record.theoretical_qty
            adjustment_cost = adjusted_qty * record.product_id.standard_price
            record.adjustment_cost = adjustment_cost
