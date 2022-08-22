odoo.define('website_sale_extended.VariantMixin', function (require) {
    'use strict';

    var VariantMixin = require('sale.VariantMixin');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var QWeb = core.qweb;
    VariantMixin.xml_load = ajax.loadXML(
        '/website_sale_extended/static/src/xml/website_sale_stock_product_availability.xml',
        QWeb
    );

});
