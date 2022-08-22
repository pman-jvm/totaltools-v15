# -*- coding: utf-8 -*-

{
    'name': 'Sales : Salesmen Access',
    'category': 'Sales/Sales',
    'summary': 'Modification on the salesman access',
    'version': '15.0',
    'description': """Enable limitation for Salesman to view only needed information""",
    'depends': ['crm', 'stock_account', 'purchase', 'point_of_sale', 'website_sale', 'professional_templates', 'website_google_merchant_center'],
    'data': [
        'security/ir.model.access.csv',

        'data/ir_rule.xml',
        'data/ir_model_access.xml',
        'security/custom_security.xml',

        'views/product_view.xml',
        'views/sale_views.xml',

    ],
    'author': 'TeqStars',
    'website': 'https://teqstars.com',
    'support': 'support@teqstars.com',
    'maintainer': 'TeqStars',
    'images': ['static/description/icon.png'],
    'installable': True,
    'uninstall_hook': 'uninstall_hook',
}
