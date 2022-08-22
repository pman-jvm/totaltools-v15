from odoo import models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_revaluation(self):
        self.ensure_one()
        ctx = dict(self._context, default_product_id=self.id, default_company_id=self.env.company.id)
        return {
            'name': _("Product Revaluation"),
            'view_mode': 'form',
            'res_model': 'stock.valuation.layer.revaluation',
            'view_id': self.env.ref('stock_revaluation.stock_revaluation_form_view').id,
            'type': 'ir.actions.act_window',
            'context': ctx,
            'target': 'new'
        }
