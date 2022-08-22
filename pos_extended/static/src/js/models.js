odoo.define('pos_extended.extended_ts', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;
    const { Gui } = require('point_of_sale.Gui');
    var DiscountButton = require("pos_discount.DiscountButton");

    models.load_models([{
        model: 'res.groups',
        fields: ['name'],
        loaded: function (self, res_group) {
            self.res_group = res_group;
        }
    },
    ]);

models.load_fields("product.product", ["qty_available", "detailed_type"]);

    var orderline_super = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({

        is_pos_group: function () {
            var groups = self.posmodel.res_group
            for (var i = 0; i < groups.length; i++) {
                if (groups[i].name === "POS Limited Discount Upto 10%" && self.posmodel.user.groups_id.includes(groups[i].id)) {
                    return true
                }
            }
            return false
        },

        set_discount: function (discount) {
            var disc = Math.min(Math.max(parseFloat(discount) || 0, 0), 100);
            if (this.is_pos_group() && disc > 10) {
                Gui.showPopup('ErrorPopup', { title: _t('Warning!!!'), body: _t("You cannot give discount more than 10%!!!") });
                return false
            }
            orderline_super.set_discount.apply(this, arguments);
        },
    });

    var order_super = models.Order.prototype;
    models.Order = models.Order.extend({

        is_pos_restrict_zero_qty_product_sale_group: function () {
            var groups = self.posmodel.res_group
            for (var i = 0; i < groups.length; i++) {
                if (groups[i].name === "POS Restrict Out Of Stock Sale" && self.posmodel.user.groups_id.includes(groups[i].id)) {
                    return true
                }
            }
            return false
        },

        add_product: function(product, options){
            if (this.is_pos_restrict_zero_qty_product_sale_group() && product.qty_available <= 0 && product.detailed_type == 'product') {
                Gui.showPopup('ErrorPopup', { title: _t("Warning!!!"), body: _t("You cannot sale out of stock product!!!") });
                return false
            }
            order_super.add_product.apply(this, arguments);
        },
    });

//    Override Method
    DiscountButton.prototype.apply_discount = function(pc) {
        const superMethod = this._super;
        var groups = self.posmodel.res_group
        if (pc > 10){
            for (var i = 0; i < groups.length; i++) {
                if (groups[i].name === "POS Limited Discount Upto 10%" && self.posmodel.user.groups_id.includes(groups[i].id)) {
                    Gui.showPopup('ErrorPopup', { title: _t("Warning!!!"), body: _t("You cannot give discount more than 10%!!!") });
                    return;
                }
            }
        }
        var order    = this.env.pos.get_order();
        var lines    = order.get_orderlines();
        var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
        if (product === undefined) {
            Gui.showPopup('ErrorPopup', { title: _t("No discount product found"), body: _t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'.") });
            return;
        }

        // Remove existing discounts
        for (const line of lines) {
            if (line.get_product() === product) {
                order.remove_orderline(line);
            }
        }

        // Add discount
        // We add the price as manually set to avoid recomputation when changing customer.
        var base_to_discount = order.get_total_without_tax();
        if (product.taxes_id.length){
            var first_tax = this.env.pos.taxes_by_id[product.taxes_id[0]];
            if (first_tax.price_include) {
                base_to_discount = order.get_total_with_tax();
            }
        }
        var discount = - pc / 100.0 * base_to_discount;

        if( discount < 0 ){
            order.add_product(product, {
                price: discount,
                lst_price: discount,
                extras: {
                    price_manually_set: true,
                },
            });
        }

    }

});