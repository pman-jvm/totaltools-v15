{
    'name': 'Web Disable Action',
    'version': '15.0',
    'license': 'AGPL-3',
    # Author
    'author': 'TeqStars',
    'website': 'https://teqstars.com',
    'support': 'info@teqstars.com',
    'maintainer': 'TeqStars',
    'category': 'Web',
    'depends': [
        'web',
    ],
    'data': [
        'security/groups.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'web_disable_action/static/src/js/list_view.js',
        ],
    },

    'installable': True,
}
