from odoo import fields, models


class MassMailingList(models.Model):
    _inherit = 'mailing.list'

    send_subscribe_mail = fields.Boolean("Send Subscribe Mail", default=True)
    template_id = fields.Many2one('mail.template', string='Email Template')
