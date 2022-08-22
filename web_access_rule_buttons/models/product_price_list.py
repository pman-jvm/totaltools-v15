from odoo import models, api, _
from odoo.exceptions import UserError


class ProductPricelistReport(models.AbstractModel):
    _inherit = 'report.product.report_pricelist'

    @api.model
    def get_html(self, data):
        if self.env.user.has_group('web_access_rule_buttons.restrict_edit_create_button'):
            raise UserError(_("You don't have access rights to print this report. Please contact your Administrator."))
        res = super(ProductPricelistReport, self).get_html(data)
        return res
