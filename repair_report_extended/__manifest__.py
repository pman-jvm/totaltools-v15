# -*- coding: utf-8 -*-
{
    'name': 'Repair Report Extended',
    'version': '15.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Added Odoo default and classic template style in professional style setting popup for repair Quotation / Order report.',

    'depends': ['repair', 'professional_templates'],

    'data': [
        'views/report_settings.xml',
        'report/repair_report.xml',
        'report/repair_order_template.xml',
        'report/classic_template.xml',
        'report/odoo_template.xml',
        'report/order_lines.xml',
    ],

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
