from odoo import fields, models, _


class MassMailingContact(models.Model):
    _inherit = "mailing.contact"

    phone = fields.Char('Phone')
