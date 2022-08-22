# -*- coding: utf-8 -*-
{
    'name': 'Mobicred Integration',
    'version': '15.0',
    'summary': 'Mobicred',
    'category': 'Website/Website',

    'depends': ['website_sale'],
    'data': [
        'views/product_details_template_view.xml'
    ],

    'images': [''],
    # Author
    'author': 'TeqStars',
    'website': 'https://teqstars.com',
    'support': 'info@teqstars.com',
    'maintainer': 'TeqStars',

    "assets": {
        "web.assets_frontend": [
            "mobicred_website/static/src/js/mobicred_emi_detail.js",
            "mobicred_website/static/src/lib/instalment.js"
        ],
        "web.assets_qweb": [
            "mobicred_website/static/src/xml/widget_template.xml"
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
