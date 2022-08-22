odoo.define("web_disable_action.ListView", function(require) {
"use strict";

    var core = require("web.core");
    var session = require("web.session");
    var ListView = require('web.ListView');
    var _t = core._t;

    ListView.include({
       init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            if (!session.is_superuser && !session.group_export_data){
                this.controllerParams.activeActions.export_xlsx = false;
            }
       }
    });
});
