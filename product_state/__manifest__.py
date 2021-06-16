# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product State",
    "summary": """
        Module introducing a state field on product template""",
    "author": "ACSONE SA/NV, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Product",
    "version": "12.0.2.0.2",
    "license": "AGPL-3",
    "depends": ["sale", "product"],
    "data": [
        "data/product_state_data.xml",
        "security/ir.model.access.csv",
        "views/product_views.xml",
    ],
    "maintainers": ["emagdalenaC2i"],
    "post_init_hook": "post_init_hook",
}
