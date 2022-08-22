from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    cover_page_pdf = fields.Binary('Cover Page', help='Add page in catalog pricelist report.')
