from odoo import models, _


class Website(models.Model):
    _inherit = 'website'

    def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False):
        order = super(Website, self).sale_get_order(force_create, code, update_pricelist, force_pricelist)
        if order.order_line:
            for line in order.order_line:
                if line.product_id.pack_size_id:
                    line.product_uom = line.product_id.pack_size_id
        return order
