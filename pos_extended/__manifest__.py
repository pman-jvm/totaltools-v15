# -*- coding: utf-8 -*-
{
    'name': 'POS Extended',
    'version': '15.0',
    'category': 'Sales/Point Of Sale',
    'description': """
    - Restrict discount for selected users to 10%.
    """,

    'depends': ['point_of_sale', 'website_sale_extended', 'pos_discount'],
    'data': [
        'security/custom_security.xml',
        'views/product_views.xml',
    ],

    # Author
    'author': 'TeqStars',
    'website': 'https://teqstars.com',
    'support': 'info@teqstars.com',
    'maintainer': 'TeqStars',

    'assets': {
        'point_of_sale.assets': [
            'pos_extended/static/src/js/models.js',
        ],
    },

    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
