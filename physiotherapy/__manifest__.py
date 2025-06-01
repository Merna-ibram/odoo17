# -*- coding: utf-8 -*-
{
    'name': "physiotherapy",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'version': '0.1',
    'license': 'LGPL-3',
    'application': True,

    'depends': [
        'base',
    ],

    'data': [
        # Security
        'security/ir.model.access.csv',


        # Data


        # Views
        'views/base_menu.xml',
        'views/registration_view.xml',



        # Wizards


        # Reports
        'reports/registration_report.xml',

    ],


}
