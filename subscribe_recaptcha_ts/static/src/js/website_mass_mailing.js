odoo.define('subscribe_recaptcha_ts.subscribe_recaptcha', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var publicWidget = require('web.public.widget');
    var _t = core._t;

    var Subscribe = publicWidget.registry.subscribe;
    ajax.loadJS("https://www.google.com/recaptcha/api.js")
    Subscribe.include({

        read_events: _.extend({
            'click .js_subscribe_btn': '_onSubscribeClick',
        }, Subscribe.prototype.read_events),

        _process_subscription: function () {
            self = this;
            var $email = this.$(".js_subscribe_email:visible");
            var cust_name = document.getElementById('customer_name')
            this.$target.removeClass('o_has_error').find('.form-control').removeClass('is-invalid');
            this._rpc({
                route: '/website_mass_mailing/subscribe',
                params: {
                    'list_id': this.$target.data('list-id'),
                    'email': $email.length ? $email.val() : false,
                    'cust_name': cust_name && cust_name.name || ''
                },
            }).then(function (result) {
                self.$(".js_subscribe_btn").addClass('d-none');
                self.$(".js_subscribed_btn").removeClass('d-none');
                self.$('input.js_subscribe_email').prop('disabled', !!result);
                if (self.$popup.length) {
                    self.$popup.modal('hide');
                }
                self.displayNotification({
                    type: 'success',
                    title: _t("Success"),
                    message: result.toast_content,
                    sticky: true,
                });
            });
        },

        _submitSubscribe: function (dialog) {
            var self = this;
            var v = grecaptcha.getResponse();
            var customer_name = document.getElementById('customer_name').value
            if (! customer_name) {
                document.getElementById('recaptcha-status').innerHTML = "Please enter your Full Name.";
                return false;
            }
            if (v.length === 0) {
                document.getElementById('recaptcha-status').innerHTML = "Please verify Captcha.";
                return false;
            } else {
                self._process_subscription();
                dialog.close();
                return true;
            }
        },
        _open_captcha_popup: function (result) {
            self = this;
            var content = '<center><div class="col-xl-6">'+
                                '<div class="row"><label class="col-form-label">First & Last Name</label>'+
                                '<input id="customer_name" class="form-control" placeholder="Enter your First & Last Name" title="Please fill in your Full Name"/></div></center>'+
                            '</div><center><div id="captcha2"/><h3 class="text-alpha" id="recaptcha-status"></h3></center>'
            var dialog = new Dialog(this, {
                title: _t("Subscribe Newsletter"),
                size: 'medium',
                $content: content,
                buttons: [
                    {
                        text: _t("Submit"),
                        classes: 'btn-primary custom_submit',
                        click: function () {
                            self._submitSubscribe(dialog);
                        },
                    },
                    {
                        text: _t("Cancel"),
                        close: true,
                    },
                ],
            });
            dialog.opened().then(function () {
                grecaptcha.render("captcha2", {
                    sitekey: result.recaptcha_key,
                    theme: "light"
                });
            });
            dialog.open()
        },

        _onSubscribeClick: function () {
            var self = this;
            var $email = this.$(".js_subscribe_email:visible");

            if ($email.length && !$email.val().match(/.+@.+/)) {
                this.$target.addClass('o_has_error').find('.form-control').addClass('is-invalid');
                return false;
            }
            self._rpc({
                route: '/website_mass_mailing/get_google_recaptcha_key',
                params: {},
            }).then(function (result) {
                if (result.recaptcha_key) {
                    self._open_captcha_popup(result);
                } else {
                    self._process_subscription();
                }
            });
        },
    });
});
