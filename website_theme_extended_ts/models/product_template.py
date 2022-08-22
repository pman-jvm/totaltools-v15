from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    doc_ids = fields.One2many('custom.url', 'product_tmpl_id', string='Documents', help="Upload documents that will display in website product page.")
