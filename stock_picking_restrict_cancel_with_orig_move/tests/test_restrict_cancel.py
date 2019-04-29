# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import SavepointCase
from odoo.exceptions import UserError


class TestRestrictCancelStockMove(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env.ref('stock.warehouse0')
        cls.warehouse.write({'reception_steps': 'three_steps'})
        cls.stock_loc = cls.warehouse.lot_stock_id
        cls.input_loc = cls.warehouse.wh_input_stock_loc_id
        cls.qc_loc = cls.warehouse.wh_qc_stock_loc_id

        cls.internal_pt = cls.warehouse.int_type_id
        cls.internal_pt.active = True

        cls.dummy_product = cls.env['product.template'].create({
            'name': 'Dummy product',
            'type': 'product',
            'purchase_ok': True,
        }).product_variant_ids

        cls.input_to_qc_picking = cls.env['stock.picking'].create({
            'picking_type_id': cls.internal_pt.id,
            'location_id': cls.input_loc.id,
            'location_dest_id': cls.qc_loc.id,
            'move_lines': [(0, 0, {
                'name': cls.dummy_product.name,
                'product_id': cls.dummy_product.id,
                'product_uom': cls.env.ref('uom.product_uom_unit').id,
                'product_uom_qty': 1,
            })]
        })
        cls.input_to_qc_picking.action_confirm()

    def test_restrict(self):
        qc_to_stock_move = self.env['stock.move'].search([
            ('product_id', '=', self.dummy_product.id),
            ('location_id', '=', self.qc_loc.id),
            ('location_dest_id', '=', self.stock_loc.id),
        ])
        qc_to_stock_picking = qc_to_stock_move.picking_id
        self.assertNotEqual(qc_to_stock_move.state, 'cancel')
        self.assertNotEqual(self.input_to_qc_picking.move_lines.state,
                            'cancel')
        with self.assertRaises(UserError):
            qc_to_stock_picking.action_cancel()
        self.input_to_qc_picking.action_cancel()
        self.assertEqual(qc_to_stock_move.state, 'cancel')
        self.assertEqual(self.input_to_qc_picking.move_lines.state, 'cancel')

    def test_do_not_restrict(self):
        # When this picking is created, odoo will apply push rules on each
        # stock move to generate putaway moves. These putaway moves are created
        # first by copying each input moves, before being merged together, thus
        # trigger a move cancellation which should be allowed anyway.
        pick = self.env['stock.picking'].create({
            'picking_type_id': self.internal_pt.id,
            'location_id': self.input_loc.id,
            'location_dest_id': self.qc_loc.id,
            'move_lines': [(0, 0, {
                'name': self.dummy_product.name,
                'product_id': self.dummy_product.id,
                'product_uom': self.env.ref('uom.product_uom_unit').id,
                'product_uom_qty': 1,
            }), (0, 0, {
                'name': self.dummy_product.name,
                'product_id': self.dummy_product.id,
                'product_uom': self.env.ref('uom.product_uom_unit').id,
                'product_uom_qty': 3,
            })]
        })
        pick.action_confirm()
        qc_to_stock_move = self.env['stock.move'].search([
            ('product_id', '=', self.dummy_product.id),
            ('location_id', '=', self.qc_loc.id),
            ('location_dest_id', '=', self.stock_loc.id),
        ])
        # qc_to_stock_move has merged all the moves so its quantity is 5
        self.assertEqual(qc_to_stock_move.product_uom_qty, 5)
