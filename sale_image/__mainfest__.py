{
    'name': 'Sale Product Image',
    'version': '1.0',
    'category': 'Sales',
    'depends': ['sale', 'base'],
    'data': [
        'views/sale_order_views.xml',
        'report/sale_order_templates.xml',
        'views/res_config_settings_view.xml',
        'views/config_settings.xml',
    ],
    'installable': True,
    'application': False,
}
