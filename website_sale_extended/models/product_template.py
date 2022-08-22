from odoo import fields, models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pack_size_id = fields.Many2one('uom.uom', string="Pack Size")

    def action_publish_products(self):
        if self.env.user.has_group('web_access_rule_buttons.restrict_edit_create_button'):
            raise UserError(_("You don't have access rights to published product. Please contact your Administrator."))
        not_published_product_ids = self.filtered(lambda p: not p.is_published and p.sale_ok)
        not_published_product_ids and not_published_product_ids.write({'is_published': True})
        return {}

    def action_unpublish_products(self):
        if self.env.user.has_group('web_access_rule_buttons.restrict_edit_create_button'):
            raise UserError(_("You don't have access rights to unpublished product. Please contact your Administrator."))
        published_product_ids = self.filtered(lambda p: p.is_published and p.sale_ok)
        published_product_ids and published_product_ids.write({'is_published': False})
        return {}

    def write(self, vals):
        if self.env.user.has_group('web_access_rule_buttons.restrict_edit_create_button') and 'website_published' in vals:
            raise UserError(_("You don't have access rights to published or unpublished product. Please contact your Administrator."))
        res = super(ProductTemplate, self).write(vals)
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # def show_qty_message_in_website_product(self):
    #     res = False
    #     inventory = self.env['stock.inventory'].search([('state', '=', 'confirm')], limit=1)
    #     if inventory and self in inventory.product_ids:
    #         res = True
    #     return res
