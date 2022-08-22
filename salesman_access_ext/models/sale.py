from odoo import api, models, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('discount')
    def _onchange_discount(self):
        if self.env.user.has_group('salesman_access_ext.group_modify_price_limit_discount'):
            if self.discount > 2.5:
                raise UserError("Discount Should be Upto 2.5%")
