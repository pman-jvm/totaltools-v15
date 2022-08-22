import json
import base64
from odoo import models
from odoo.tools import date_utils


class PosCache(models.Model):
    _inherit = 'pos.cache'

    def refresh_cache(self):
        for cache in self:
            Product = self.env['product.product'].with_user(cache.compute_user_id.id)
            products = Product.search(cache.get_product_domain())
            prod_ctx = products.with_context(pricelist=cache.config_id.pricelist_id.id, location=cache.config_id.default_location_src_id.id, compute_child=False,
                                             display_default_code=False, lang=cache.compute_user_id.lang)
            res = prod_ctx.read(cache.get_product_fields())
            cache.write({
                'cache': base64.encodebytes(json.dumps(res, default=date_utils.json_default).encode('utf-8')),
            })
