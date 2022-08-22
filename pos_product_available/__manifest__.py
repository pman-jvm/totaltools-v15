# Copyright 2014-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2017 Gabbasov Dinar <https://it-projects.info/team/GabbasovDinar>
# Copyright 2018-2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """POS: show product qty""",
    "summary": """Adds available quantity at products in POS""",
    "category": "Point Of Sale",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version={ODOO_BRANCH}",
    "images": ["images/pos_product_available.jpg"],
    "version": "15.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev, TeqStars",
    "support": "pos@it-projects.info, info@teqstars.com",
    "website": "https://apps.odoo.com/apps/modules/13.0/pos_product_available/, https://teqstars.com",
    "license": "Other OSI approved licence",  # MIT
    # "price": 9.00,
    # "currency": "EUR",
    "depends": ["point_of_sale", "stock", "pos_cache"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["views/views.xml"],
    'assets': {
        'point_of_sale.assets': [
            'pos_product_available/static/src/js/pos.js',
            'pos_product_available/static/src/css/pos.css',
        ],
        'web.assets_backend': [
            'pos_product_available/static/src/js/test_pos_quantities.js',
        ],
    },
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
