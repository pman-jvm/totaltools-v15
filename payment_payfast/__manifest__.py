# -*- coding: utf-8 -*-
{
    'name': 'PayFast Payment',
    'category': 'ecommerce',
    'summary': 'Payment Acquirer: PayFast Implementation',
    'version': '15.0',
    'description': '''Make your transaction through PayFast''',
    'license': 'OPL-1',
    'author': 'DRC Systems India Pvt. Ltd., TeqStars',
    'website': 'www.drcsystems.com, https://teqstars.com',
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_payfast_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': ['static/src/img/payfast.png'],
    'installable': True,
    'price': 40,
    'currency': 'EUR',
    'support': 'support@drcsystems.com, support@teqstars.com',
}
