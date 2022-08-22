odoo.define('mobicred_website.mobicred_emi_detail', function(require) {
    'use strict';

require('website_sale.website_sale');
const publicWidget = require('web.public.widget');
const sAnimations = require('website.content.snippets.animation');
const Dialog = require('web.Dialog');
const core = require('web.core');
const QWeb = core.qweb;
const _t = core._t;

publicWidget.registry.WebsiteSale.include({
    xmlDependencies: (publicWidget.registry.WebsiteSale.prototype.xmlDependencies || []).concat(
        ['/mobicred_website/static/src/xml/widget_template.xml']
    ),
    events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events || {}, {
        'click .js_mobicred_info': '_onOpenEMIDetails',
    }),

    _onOpenEMIDetails: function (ev) {
        ev.stopPropagation();
        this.$modal = $(QWeb.render('mobicred_website.EMIDetails', {widget:self}));
        this.$modal.appendTo('body');
        this.$modal.modal('show');
    },
});

 });