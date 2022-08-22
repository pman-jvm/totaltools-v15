# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Web Access Rules Buttons",
    "summary": "Disable Edit button if access rules prevent this action",
    "version": "15.0",
    "author": "Camptocamp, Onestein, Odoo Community Association (OCA), TeqStars",
    "license": "AGPL-3",
    "category": "Web",
    "depends": [
        "web",
        "product",
        "account_accountant",
        "sale_management",
    ],
    "website": "https://github.com/OCA/web/tree/11.0/web_access_rule_buttons, https://teqstars.com",
    "data": [
        "security/custom_security.xml",
        "views/sale_order.xml",
        "views/account_move.xml",
    ],

    'assets': {
        'web.assets_backend': [
            'web_access_rule_buttons/static/src/js/form_controller.js',
        ],
    },

    "installable": True,
}
