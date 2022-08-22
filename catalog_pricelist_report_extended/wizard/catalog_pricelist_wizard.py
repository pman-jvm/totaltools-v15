# See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class CatalogPricelistReport(models.TransientModel):
    _inherit = "catalog.pricelist.report.wizard"

    header_address = fields.Text('Address')
    print_footer_images = fields.Boolean(string="Print Footer Image")
    footer_image = fields.Binary(string='Footer Logo')
    pricelist2_id = fields.Many2one('product.pricelist', 'Pricelist2')

    @api.model
    def default_get(self, fields):
        res = super(CatalogPricelistReport, self).default_get(fields)
        res['qty_1'] = 1
        res['barcode_print'] = True
        return res

    def print_report(self):
        active_ids = self.env.context.get('active_ids', [])
        # data = self.read()[0]
        categs = self.env['product.product'].browse(active_ids).mapped('categ_id')
        report_data = {}
        for categ in categs:
            products_ids = self.env['product.product'].search([('id', 'in', active_ids), ('categ_id', '=', categ.id)])
            report_data.update({categ.id: products_ids.ids})
        return {
            'name': 'Catalog Report',
            'type': 'ir.actions.act_url',
            'url': '/print/catalog_pricelist_report_ts?report_data=%(report_data)s&wizard_id=%(wizard_id)s' % {'report_data': report_data, 'wizard_id': self.id},
        }
