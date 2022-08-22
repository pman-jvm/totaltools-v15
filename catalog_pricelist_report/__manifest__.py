# See LICENSE file for full copyright and licensing details.

{
    # Module information
    'name': 'Catalog Pricelist Report',
    'category': 'Report',
    'summary': 'Migrated the app from v13 to v15. Generated the Product Catalog Report.',
    'description': 'Product Catalog report with Barcode, Image and \
     Stock Availability and Incoming Stock.\
      Catalog Product, Barcode, Image catalog report.',
    'version': '15.0',
    'license': 'LGPL-3',
    'sequence': 1,
    # Author
    'author': 'Serpent Consulting Services Pvt. Ltd., TeqStars',
    'website': 'http://www.serpentcs.com, https://teqstars.com',

    # Dependencies
    'depends': ['sale_management', 'stock', 'purchase'],

    # Views
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'wizard/catalog_pricelist_wizard_view.xml',
        'report/catalog_report_view.xml',
        'report/report_registration.xml',
    ],
    'images': ['static/description/banner_icon.jpg'],
    # Techical
    'installable': True,
    'auto_install': False,
    'price': 29,
    'currency': 'EUR',
}
