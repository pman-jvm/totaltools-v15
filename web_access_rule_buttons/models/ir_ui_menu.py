# -*- coding: utf-8 -*-

from odoo import api, models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.returns('self')
    def _filter_visible_menus(self):
        if self.env.user and self.env.user.has_group('account.group_account_invoice') and self.env.user.id == 7:
            account_menu_id = self.env.ref('account_accountant.menu_accounting')
            self = self - account_menu_id
        res = super(IrUiMenu, self)._filter_visible_menus()
        return res
