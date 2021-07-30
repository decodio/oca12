# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def _get_next_date(self, date, qty=1):
        self.ensure_one()
        return self.product_tmpl_id._get_next_date(date, qty=qty)
