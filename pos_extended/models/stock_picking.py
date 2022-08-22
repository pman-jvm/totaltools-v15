from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _prepare_stock_move_vals(self, first_line, order_lines):
        res = super(StockPicking, self)._prepare_stock_move_vals(first_line, order_lines)
        if first_line.product_id.pack_size_id:
            res.update({'product_uom': first_line.product_id.pack_size_id.id})
        if first_line.product_id.pack_size_id:
            res.update({'product_uom_qty': first_line.product_id.pack_size_id._compute_quantity(first_line.qty, first_line.product_id.uom_id)})
        return res
