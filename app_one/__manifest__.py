{
    'name': "APP ONE",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'web', 'mail', 'sale_management', 'account_accountant', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tags_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'views/todo_task_view.xml',
        'reports/property_report.xml',

    ],


    'application': True,
    'license': 'LGPL-3',
    'assets': {
      'web.assets_backend':['app_one/static/src/css/property.css', 'app_one/static/src/css/owner.css'],
    },

}