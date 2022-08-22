/* Copyright 2016 Camptocamp SA
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("web_access_rule_buttons.main", function (require) {
    "use strict";
    var FormController = require("web.FormController");
    var ListController = require("web.ListController");
    var KanbanController = require("web.KanbanController");
    var FormRenderer = require("web.FormRenderer");

    FormController.include({

        async _onQuickEdit(ev) {
            const _super = this._super.bind(this);
            const current_session = this.getSession();
            var restrict_edit_button_for_all_models = await current_session.user_has_group('web_access_rule_buttons.restrict_edit_button')
            if (restrict_edit_button_for_all_models) {
                return;
            }
            if (['res.partner', 'product.template', 'product.product', 'product.pricelist', 'account.move'].includes(this.initialState.model)) {
                var restrict_edit_button_for_list_models = await current_session.user_has_group('web_access_rule_buttons.restrict_edit_create_button')
                if (restrict_edit_button_for_list_models){
                    return;
                }
            }
            return _super(ev)
        },

        async _update(state, params) {
            return this._super(state, params).then(this.show_hide_buttons(state));
        },
        show_hide_buttons : function (state) {
            var self = this;
            return self._rpc({
                model: this.modelName,
                method: 'check_access_rule_all',
                args: [[state.data.id], ["write","create"]],
            }).then(function (accesses) {
                self.show_hide_edit_button(accesses);
            });
        },
        show_hide_edit_button : function (access) {
            if (this.$buttons) {
                var button_edit = this.$buttons.find(".o_form_button_edit");
                var button_create = this.$buttons.find(".o_form_button_create");
                if (button_edit) {
                    button_edit.prop("disabled", !access.write);
                }
                if (button_create) {
                    button_create.prop("disabled", !access.create);
                }
            }
        },

    });

    ListController.include({

        async _update(state, params) {
            return this._super(state, params).then(this.show_hide_buttons(state));
        },
        show_hide_buttons : function (state) {
            var self = this;
            return self._rpc({
                model: this.modelName,
                method: 'check_access_rule_all',
                args: [[state.data.id], ["write","create"]],
            }).then(function (accesses) {
                self.show_hide_edit_button(accesses);
            });
        },
        show_hide_edit_button : function (access) {
            if (this.$buttons) {
                var button_create = this.$buttons.find(".o_list_button_add");
                if (button_create) {
                    button_create.prop("disabled", !access.create);
                }
            }
        },

    });

    KanbanController.include({

        async _update(state, params) {
            return this._super(state, params).then(this.show_hide_buttons(state));
        },
        show_hide_buttons : function (state) {
            var self = this;
            return self._rpc({
                model: this.modelName,
                method: 'check_access_rule_all',
                args: [[state.data.id], ["write","create"]],
            }).then(function (accesses) {
                self.show_hide_edit_button(accesses);
            });
        },
        show_hide_edit_button : function (access) {
            if (this.$buttons) {
                var button_create = this.$buttons.find(".o-kanban-button-new");
                if (button_create) {
                    button_create.prop("disabled", !access.create);
                }
            }
        },

    });

});
