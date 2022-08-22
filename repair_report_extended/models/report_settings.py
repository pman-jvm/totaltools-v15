from odoo import models, fields, api


class ProductPackaging(models.Model):
    _inherit = 'report.template.settings'

    @api.model
    def _default_repair_template(self):
        def_tpl = self.env['ir.ui.view'].search([('key', 'like', 'repair_report_extended.repair\_%\_document'), ('type', '=', 'qweb')], order='key asc', limit=1)
        return def_tpl or self.env.ref('repair.report_repairorder')

    template_repair = fields.Many2one('ir.ui.view', 'Order/Quote Template (Repair)', default=_default_repair_template,
                                      domain="[('type', '=', 'qweb'), ('key', 'like', 'repair_report_extended.repair\_%\_document' )]", required=False)
