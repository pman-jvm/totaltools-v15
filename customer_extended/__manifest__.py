# -*- coding: utf-8 -*-
{
    'name': 'Customer Extended',
    'version': '15.0',
    'category': 'Accounting',
    'summary': 'Automatic customer statement sent every months',

    'depends': ['account','account_reports'],

    'data': [
        'data/ir_cron.xml',
        'views/res_partner.xml',
        'views/report_statement.xml'
    ],

    'images': ['static/description/icon.jpg'],

    'author': 'TeqStars',
    'website': 'https://teqstars.com',
    'support': 'support@teqstars.com',
    'maintainer': 'TeqStars',

    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}