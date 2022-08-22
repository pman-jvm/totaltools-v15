{
    "name": "Execute Python Code",
    "description": """
Installing this module, user will able to execute python code from Odoo
""",
    "author": "OpenERP SA",
    "version": "0.1",
    "depends": ["base"],
    "init_xml": [],
    "data": [
        'security/ir.model.access.csv',
        'view/python_code_view.xml',
    ],
    "demo_xml": [],
    'license': 'LGPL-3',
    "installable": True,
}
