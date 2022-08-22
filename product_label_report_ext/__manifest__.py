{
    'name': "Product Label (PDF) Report Extended",
    'summary': 'Report custom modification on Product Label (PDF) report.',
    'description': """
Allow users to select pricelist and label on report shows that pricelist's pricing with related currency.
    """,
    'version': "15.0",
    'category': 'Sales/Sales',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'report/report_product_pricelist_label.xml',
        'wizard/product_label_pricelist_wizard_view.xml',
    ],
    'author': "TeqStars",
    'website': "https://teqstars.com",
    'support': 'support@teqstars.com',
    'maintainer': 'TeqStars',
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'auto_install': False,
}
