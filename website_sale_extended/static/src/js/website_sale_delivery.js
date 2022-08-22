odoo.define('website_sale_extended.checkout', function (require) {
    'use strict';

    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    require('website_sale_delivery.checkout');

    var _t = core._t;

    publicWidget.registry.websiteSaleDelivery.include({

        start: function () {
            var self = this;
            var $carriers = $('#delivery_carrier input[name="delivery_type"]');
            var $payButton = $('#o_payment_form_pay');
            // Workaround to:
            // - update the amount/error on the label at first rendering
            // - prevent clicking on 'Pay Now' if the shipper rating fails
            if ($carriers.length > 0) {
                if ($carriers.filter(':checked').length === 0) {
                    $payButton.prop('disabled', true);
                    var disabledReasons = $payButton.data('disabled_reasons') || {};
                    disabledReasons.carrier_selection = true;
                    $payButton.data('disabled_reasons', disabledReasons);
                }
                $carriers.filter(':checked').click();
            }

            // Asynchronously retrieve every carrier price
            _.each($carriers, function (carrierInput, k) {
                self._showLoading($(carrierInput));
                self._rpc({
                    route: '/shop/carrier_rate_shipment',
                    params: {
                        'carrier_id': carrierInput.value,
                    },
                }).then(self._handleCarrierUpdateResultBadge.bind(self));
            });

            return this._super.apply(this, arguments);
        },
    });
});
