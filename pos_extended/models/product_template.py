from odoo import models,fields,api
from odoo.tools.float_utils import float_round


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_qty_available = fields.Float(
        'Quantity On Hand', compute='_compute_quantities_pos',
        compute_sudo=False, digits='Product Unit of Measure')

    @api.depends_context('company_owned', 'force_company', 'location', 'warehouse')
    def _compute_quantities_pos(self):
        res = self._compute_quantities_pos_dict()
        for template in self:
            template.pos_qty_available = res[template.id]['pos_qty_available']

    def _compute_quantities_pos_dict(self):
        variants_available = self.mapped('product_variant_ids')._pos_product_available()
        prod_available = {}
        for template in self:
            pos_qty_available = 0
            for p in template.product_variant_ids:
                pos_qty_available += variants_available[p.id]["pos_qty_available"]
            prod_available[template.id] = {
                "pos_qty_available": pos_qty_available,
            }
        return prod_available


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _pos_product_available(self):
        """ Compatibility method """
        return self._compute_pos_quantities_dict()

    def _compute_pos_quantities_dict(self):
        active_pos = self.env['pos.config'].search([('active','=',True)], limit=1)
        location_id = active_pos and active_pos.picking_type_id and active_pos.picking_type_id.default_location_src_id.id or False
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations_new(location_id, company_id=self.env.context.get('force_company', False), compute_child=self.env.context.get('compute_child', True))
        domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc
        Quant = self.env['stock.quant']
        quants_res = dict((item['product_id'][0], (item['quantity'], item['reserved_quantity'])) for item in Quant.read_group(domain_quant, ['product_id', 'quantity', 'reserved_quantity'], ['product_id'], orderby='id'))
        res = dict()
        for product in self.with_context(prefetch_fields=False):
            product_id = product.id
            if not product_id:
                res[product_id] = dict.fromkeys(
                    ['pos_qty_available'],
                    0.0,
                )
                continue
            rounding = product.uom_id.rounding
            res[product_id] = {}
            qty_available_pos = quants_res.get(product_id, [0.0])[0]
            res[product_id]['pos_qty_available'] = float_round(qty_available_pos, precision_rounding=rounding)
        return res

