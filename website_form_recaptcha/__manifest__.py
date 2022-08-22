# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Form - ReCaptcha",
    "summary": "Provides a ReCaptcha field for Website Forms",
    "version": "15.0",
    "category": "Website",
    "website": "https://github.com/OCA/website, https://teqstars.com",
    "author": "LasLabs, Tecnativa, Odoo Community Association (OCA), TeqStars",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["website"],
    "data": [
        # "views/assets.xml",
        "views/website_config_settings.xml",
    ],
    "images": ["static/description/website_form_recaptcha.jpg"],
    "assets": {
        'web.assets_frontend': ['website_form_recaptcha/static/src/js/field_recaptcha.js',
                                ],
    },
}
