from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    vat_price = fields.Float('Price with VAT', compute='_compute_vat_price', digits='Product Price')

    @api.depends('lst_price', 'taxes_id')
    def _compute_vat_price(self):
        for rec in self:
            taxes = rec.taxes_id.compute_all(rec.lst_price, rec.env.user.company_id.currency_id, 1, product=rec, partner=False)
            rec.vat_price = taxes['total_included']
