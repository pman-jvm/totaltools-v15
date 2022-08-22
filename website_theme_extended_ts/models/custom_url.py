from odoo import fields, models


class CustomURL(models.Model):
    _name = "custom.url"

    name = fields.Char("Name")
    url = fields.Char("URL")
    product_tmpl_id = fields.Many2one("product.template", "Product Template")
