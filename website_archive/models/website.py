from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    active = fields.Boolean(default=True)
