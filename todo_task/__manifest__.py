{
    'name': "TO_DA APP",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'views/todo_task_line_view.xml',
        'reports/todo_report.xml',
        'wizard/todo_assignment_view.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'todo_task/static/src/components/listView/css/listView.css',
            'todo_task/static/src/components/listView/js/listView.js',
            'todo_task/static/src/components/listView/xml/listView.xml',
        ],
    },

    'application': True,

}