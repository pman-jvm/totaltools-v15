# See LICENSE file for full copyright and licensing details.
from odoo import api, models
from odoo.tools import float_round


class CatalogReport(models.AbstractModel):
    """Catalog report."""

    _name = 'report.product_label_report_ext.report_productlabel'
    _description = "Product Pricelist Label report."

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['product.product'].browse(data.get('ids'))
        pricelist_id = False
        currency_id = False
        if data.get('form') and data.get('form').get('pricelist_id'):
            pricelist_id = self.env['product.pricelist'].browse(data['form']['pricelist_id'])
            currency_id = pricelist_id.currency_id
        return {
            'doc_ids': docs,
            'doc_model': 'product.product',
            'docs': docs,
            'pricelist_id': pricelist_id,
            'currency_id': currency_id,
        }
