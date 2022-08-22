{
    "name": "Newsletter Recaptcha",
    "version": "15.0",
    "category": "Other",
    'summary': 'While customer subscribe to newsletter it popup will open and ask to put First and Last name and complete Google reCaptcha Verification',

    "depends": ['website_mass_mailing', 'website_form_recaptcha'],

    'data': [
        'views/mailing_list_views.xml'
    ],

    'images': [],

    "author": "TeqStars",
    "website": "https://teqstars.com",
    'support': 'support@teqstars.com',
    'maintainer': 'TeqStars',

    "description": """
        """,

    'assets': {
        'web.assets_frontend': [
            'subscribe_recaptcha_ts/static/src/js/website_mass_mailing.js',
        ],
    },

    'demo': [],
    'license': 'OPL-1',
    'auto_install': False,
    'installable': True,
    'application': False,
    'qweb': [],
    "price": "",
    "currency": "EUR",
}
