# -*- coding: utf-8 -*-
{
    'name': 'Theme Extended',
    'version': '15.0',
    'summary': 'Theme Extended',
    'category': 'Website/Website',

    'depends': ['theme_alan', 'auth_signup', 'delivery'],
    'data': [
        'views/website_categories_view.xml',
        'views/templates.xml',
        'views/snippets.xml',
        'views/res_company.xml',
        'views/components.xml',
        'views/product_template.xml',
        # 'views/layout.xml',

        'security/ir.model.access.csv'

    ],

    "assets": {
        'web.assets_frontend': [
            'website_theme_extended_ts/static/src/scss/custom_style.scss',
        ],
    },

    'images': [''],
    # Author
    'author': 'TeqStars',
    'website': 'https://teqstars.com',
    'support': 'info@teqstars.com',
    'maintainer': 'TeqStars',

    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
    'price': 0.00,
    'currency': 'EUR',
}
