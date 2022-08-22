# -*- coding: utf-'8' "-*-"
import logging
from urllib import parse
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.addons.payment_payfast.controllers.main import PayfastController

_logger = logging.getLogger(__name__)


class AcquirerPayFast(models.Model):
    _inherit = 'payment.acquirer'

    merchant_id = fields.Integer('Merchant ID', required_if_provider='payfast')
    merchant_key = fields.Char('Merchant Key', required_if_provider='payfast')
    provider = fields.Selection(selection_add=[('payfast', 'Payfast')], ondelete={'payfast': 'set default'})

    def _payfast_get_api_url(self):
        environment = 'prod' if self.state == 'enabled' else 'test'
        if environment == 'prod':
            return 'https://www.payfast.co.za/eng/process'
        else:
            return 'https://sandbox.payfast.co.za/eng/process'


class TxPayfast(models.Model):
    _inherit = 'payment.transaction'

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    payfast_txn_id = fields.Char(string="Payfast Transaction ID")
    request_payload = fields.Text('Request Payload')
    response_payload = fields.Text('Response Payload')

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        """ Override of payment to find the transaction based on Paypal data.
        """
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'payfast':
            return tx
        reference = data.get('custom_str1')
        tx_ids = self.search([('reference', '=', reference), ('provider', '=', 'payfast')])
        if not tx_ids or len(tx_ids) > 1:
            error_msg = 'Payfast: received data for reference %s' % (reference)
            if not tx_ids:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx_ids[0]

    def _process_feedback_data(self, data):
        """ Override of payment to process the transaction based on Paypal data.
        """
        super()._process_feedback_data(data)
        if self.provider != 'payfast':
            return
        self.write({'payfast_txn_id': data['pf_payment_id']})
        if data['status'] == 'COMPLETE':
            self._set_done()
        else:
            self._set_error("payFast: " + _("Received data with invalid payment status"))

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Paypal-specific rendering values.
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider != 'payfast':
            return res
        item_name = ''
        self.request_payload = processing_values
        sale_orders = self.sale_order_ids
        for sale_order in sale_orders:
            for line in sale_order.order_line:
                item_name = item_name + line.product_id.name + '_'

        # Can be other item then sale order
        if not item_name:
            item_name = self.reference
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        payfast_tx_values = dict(processing_values)
        payfast_tx_values.update({
            'merchant_id': self.acquirer_id.merchant_id,
            'merchant_key': self.acquirer_id.merchant_key,
            'amount': round(self.amount, 2),
            'item_name': item_name,
            'return_url': '%s' % parse.urljoin(base_url, PayfastController.return_url),
            'cancel_url': '%s' % parse.urljoin(base_url, PayfastController.cancel_url),
            'notify_url': '%s' % parse.urljoin(base_url, PayfastController.notify_url),
            'custom_str1': self.reference,
            'api_url': self.acquirer_id._payfast_get_api_url(),
        })
        return payfast_tx_values
