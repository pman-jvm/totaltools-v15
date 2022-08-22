# See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ProductLabelPricelist(models.TransientModel):
    _name = "product.label.pricelist"
    _description = 'Product Label Pricelist'

    pricelist_id = fields.Many2one('product.pricelist')

    def print_report(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'product.product',
            'form': {'pricelist_id': self.pricelist_id.id}
        }
        return self.env.ref('product_label_report_ext.report_product_label').report_action([], data=datas)
