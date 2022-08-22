import logging

from odoo import fields, models, _

_logger = logging.getLogger(__name__)


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    product_uom_id = fields.Many2one('uom.uom', string='Product UoM', related='')

    def _order_line_fields(self, line, session_id=None):
        res = super(PosOrderLine, self)._order_line_fields(line, session_id)
        product = self.env['product.product'].search([('id', '=', res[2].get('product_id'))])
        if product.pack_size_id:
            res[2]['product_uom_id'] = product.pack_size_id.id
        else:
            res[2].update({'product_uom_id': product.uom_id.id})
        return res
