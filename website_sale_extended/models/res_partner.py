from odoo import fields, models, _


class Partner(models.Model):
    _inherit = 'res.partner'

    unit_number = fields.Char('Unit Number')
    complex_name = fields.Char('Complex Name')