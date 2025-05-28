# -*- coding: utf-8 -*-
{
    'name': "APP ONE",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Sales',
    'version': '0.1',
    'license': 'LGPL-3',
    'application': True,

    'depends': [
        'base',
        'web',
        'mail',
        'sale',
        'sale_management',
        'account_accountant',
        'contacts',
    ],

    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',

        # Data
        'data/sequence.xml',
        'data/data.xml',

        # Views
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/property_history_view.xml',
        'views/owner_view.xml',
        'views/building_view.xml',
        'views/tags_view.xml',
        'views/sale_order_view.xml',
        'views/sale_order_line_view.xml',
        'views/res_partner_view.xml',
        'views/account_move_view.xml',

        # Wizards
        'wizard/property_change_state_view.xml',

        # Reports
        'reports/property_report.xml',
        'reports/sale_order_report.xml',
    ],

    'assets': {
        'web.report_assets_common': [
            'app_one/static/src/css/property.css',
            'app_one/static/src/css/font.css',
        ],
        'web.assets_backend': [
            'app_one/static/src/css/property.css',
            'app_one/static/src/css/owner.css',
            'app_one/static/src/components/listView/css/listView.css',
            'app_one/static/src/components/listView/js/listView.js',
            'app_one/static/src/components/listView/xml/listView.xml',
            'app_one/static/src/components/listView/css/owner_listView.css',
            'app_one/static/src/components/listView/js/owner_listView.js',
            'app_one/static/src/components/listView/xml/owner_listView.xml',
        ],
    },
}
