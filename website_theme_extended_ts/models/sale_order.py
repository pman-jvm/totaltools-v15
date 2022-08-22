# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_free_delivery_total_amount(self):
        amounts = []
        for carrier in self.env['delivery.carrier'].sudo().search([('is_published', '=', True), ('free_over', '=', True)]):
            amounts.append(carrier.amount)
        if amounts:
            min_amount = min(amounts)
            if self.amount_total >= min_amount:
                return False
            return min_amount - self.amount_total
        return False
