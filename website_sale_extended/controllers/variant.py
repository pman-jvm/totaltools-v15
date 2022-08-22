# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request

from odoo.addons.sale.controllers.variant import VariantController


class ProductSpecificationSaleVariantController(VariantController):

    @http.route(['/sale/get_combination_info'], type='json', auth="user", methods=['POST'])
    def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
        res = super(ProductSpecificationSaleVariantController, self).get_combination_info(
            product_template_id=product_template_id, product_id=product_id, combination=combination, add_qty=add_qty,
            pricelist_id=pricelist_id, **kw)
        default_code = ''
        if res.get('product_id', False):
            product = request.env['product.product'].sudo().browse(res['product_id'])
            default_code = product.default_code or ''
        res['default_code'] = default_code
        return res
