# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, exceptions


class Base(models.AbstractModel):
    """ The base model, which is implicitly inherited by all models. """
    _inherit = 'base'

    def check_access_rule_all(self, operations=None):
        """Verifies that the operation given by ``operations`` is allowed for
        the user according to ir.rules.

        If ``operations`` is empty, it returns the result for all actions.

       :param operation: a list of ``read``, ``create``, ``write``, ``unlink``
       :return: {operation: access} (access is a boolean)
        """
        if not operations or not any(operations):
            operations = ['read', 'create', 'write', 'unlink']
        result = {}
        for operation in operations:
            if self.env.user.has_group('web_access_rule_buttons.restrict_edit_button') and operation == 'write':
                result[operation] = False
                continue
            if self.env.user.has_group('web_access_rule_buttons.restrict_edit_create_button') and self._name in ['res.partner', 'product.template', 'product.product', 'product.pricelist',
                                                                                                                 'account.move']:
                result[operation] = False
                continue
            if self.is_transient() or not self.ids:
                # If we call check_access_rule() without id, it will try to
                # run a SELECT without ID which will crash, so we just blindly
                # allow the operations
                result[operation] = True
                continue
            try:
                self.check_access_rule(operation)
            except exceptions.AccessError:
                result[operation] = False
            else:
                result[operation] = True
        action_report = self.env['ir.actions.report'].search([('model', 'in', ['product.template', 'product.product'])])
        if self.env.user.has_group('web_access_rule_buttons.restrict_edit_create_button') and self._name in ['product.template', 'product.product']:
            action_report.sudo().unlink_action()
        else:
            action_report.sudo().create_action()
        return result
