from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleExtended(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, kw):
        checkout['unit_number'] = kw.get('unit_number')
        checkout['complex_name'] = kw.get('complex_name')
        partner_id = super(WebsiteSaleExtended, self)._checkout_form_save(mode, checkout, kw)
        return partner_id
