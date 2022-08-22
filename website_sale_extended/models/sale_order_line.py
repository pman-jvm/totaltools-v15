from odoo import api, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id.pack_size_id:
            self.write({'product_uom': self.product_id.pack_size_id.id})
        return res

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if self.product_id.pack_size_id == self.product_uom:
            if self.order_id.pricelist_id and self.order_id.partner_id:
                product = self.product_id.with_context(
                    lang=self.order_id.partner_id.lang,
                    partner=self.order_id.partner_id,
                    quantity=self.product_uom_qty,
                    date=self.order_id.date_order,
                    pricelist=self.order_id.pricelist_id.id,
                    fiscal_position=self.env.context.get('fiscal_position'))
                self.price_unit = product.price
        else:
            super(SaleOrderLine, self).product_uom_change()

    def _get_display_price(self, product):
        res = super(SaleOrderLine, self)._get_display_price(product)
        if self.product_uom == self.product_id.pack_size_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                fiscal_position=self.env.context.get('fiscal_position'))
            res = product.price
        return res
