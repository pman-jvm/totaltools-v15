odoo.define('website_sale_extended.modified_the_product_add_to_cart_ts', function(require) {
    'use strict';

require('website_sale.website_sale');
const sAnimations = require('website.content.snippets.animation');
const publicWidget = require('web.public.widget');
const Dialog = require('web.Dialog');
const core = require('web.core');
const QWeb = core.qweb;
const _t = core._t;

publicWidget.registry.WebsiteSale.include({
    xmlDependencies: (publicWidget.registry.WebsiteSale.prototype.xmlDependencies || []).concat(
        ['/website_sale_extended/static/src/xml/widget_template.xml']
    ),
    events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events || {}, {
        'click .product_detail_img': '_onOpenImageView',
    }),

    _onOpenImageView: function (ev) {
        ev.stopPropagation();
        this.src = $(ev.currentTarget).attr('src');
//            var id_of_cart = $(ev.currentTarget).parents('div:first').parents('div:first').parents('div:first').parents('div:first').parents('div:first').attr('id')
        var id_of_cart = this.$el.find('#o-carousel-product')
        if (this.src && id_of_cart.length){
            this.$modal = $(QWeb.render('website_sale_extended.ProductImagePreview', {url: this.src}));
            this.$modal.appendTo('body');
            this.$modal.modal('show');
        }
    },
});

});