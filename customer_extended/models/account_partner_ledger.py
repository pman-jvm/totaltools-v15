from odoo import models, api, _


class AccountPartnerLedger(models.AbstractModel):
    _inherit = "account.partner.ledger"

    @api.model
    def _get_options(self, previous_options=None):
        if self.filter_date and self._context.get('auto_send_statement', False):
            self.filter_date.update({'filter': 'last_month'})
        res = super(AccountPartnerLedger, self)._get_options(previous_options)
        return res

    @api.model
    def _get_report_name(self):
        return _('Statement')
