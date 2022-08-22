 # -*- coding: utf-8 -*-
from odoo import models, fields, _


class ResCompany(models.Model):
    _inherit = "res.company"

    phone2 = fields.Char('Phone2')
    phone3 = fields.Char('Phone3')