# See LICENSE file for full copyright and licensing details.
from odoo import api, models


class CatalogReport(models.AbstractModel):
    """Catalog report."""

    _inherit = 'report.catalog_pricelist_report.catalog_report'

    def _get_categorie_data(self, products, product_quantities, pricelist, pricelist2, include_tax):
        categ_lst = []
        categories_data = self.env['product.category']
        for product in products:
            categories_data |= product.categ_id
        for category in categories_data:
            products_categ = products.filtered(lambda product: product.categ_id == category)
            prices = {}
            prices2 = {}
            for categ_product in products_categ:
                prices[categ_product.id] = dict.fromkeys(product_quantities, 0.0)
                prices2[categ_product.id] = dict.fromkeys(product_quantities, 0.0)
                for quantity in product_quantities:
                    prices[categ_product.id][quantity] = self._get_price_data(pricelist, categ_product, quantity, include_tax)
                    prices2[categ_product.id][quantity] = self._get_price_data(pricelist2, categ_product, quantity, include_tax)
            categ_lst.append({
                'category': category,
                'products': products_categ,
                'prices': prices,
                'prices2': prices2,
            })
        return categ_lst

    @api.model
    def _get_report_values(self, docids, data=None):
        rate = 0.0
        pricelist = False
        pricelist2 = False
        symbol = ''
        currency_name = ''
        pricelist_name = ''
        currency_name2, symbol2, pricelist2_name = '', '', ''
        docs = self.env['product.product'].browse(data.get('ids'))
        product_quantities = self._quantity(data)
        include_tax = False
        if data['form']['include_tax']:
            include_tax = data['form']['include_tax']
        if data['form']['pricelist_id']:
            pricelist = self.env['product.pricelist'].browse(data['form']['pricelist_id'][0])
            pricelist_name = pricelist.name
            currency_name = pricelist and pricelist.currency_id.name or False
            symbol = pricelist.currency_id.symbol or False
        if data['form']['pricelist2_id']:
            pricelist2 = self.env['product.pricelist'].browse(data['form']['pricelist2_id'][0])
            pricelist2_name = pricelist2.name
            currency_name2 = pricelist2 and pricelist2.currency_id.name or False
            symbol2 = pricelist2.currency_id.symbol or False
        return {
            'doc_ids': docs,
            'doc_model': 'product.product',
            'docs': docs,
            'test': data,
            'rate': rate or 00,
            'symbol': symbol or False,
            'currency_name': currency_name or False,
            'pricelist_name': pricelist_name or False,
            'symbol2': symbol2 or False,
            'currency_name2': currency_name2 or False,
            'pricelist2_name': pricelist2_name or False,
            'data': dict(data, quantities=product_quantities, categories_data=self._get_categorie_data(docs, product_quantities, pricelist, pricelist2, include_tax)
                         ),
        }
