# -*- coding: utf-8 -*-
{
    'name': 'Website Sale Extended',
    'version': '15.0',
    'summary': 'Added SKU in the add to cart page',
    'category': 'Website/Website',

    'depends': ['web_access_rule_buttons', 'website_sale_delivery'],
    'data': [
        'views/product_add_cart_template.xml',
        'views/partner_address_template.xml',
        'views/res_partner.xml',
        'views/website_templates.xml',
        'views/product_template.xml',
    ],

    'images': [''],
    # Author
    'author': 'TeqStars',
    'website': 'https://teqstars.com',
    'support': 'info@teqstars.com',
    'maintainer': 'TeqStars',

    "assets": {
        "web.assets_frontend": [
            "website_sale_extended/static/src/js/website_add_to_cart_modification_new.js",
            "website_sale_extended/static/src/js/website_sale_delivery.js",
            "website_sale_extended/static/src/js/variant_mixin.js",
        ],
        "web.assets_qweb": [
            "website_sale_extended/static/src/xml/*.xml",
        ]
    },

    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
    'price': 0.00,
    'currency': 'EUR',
}
