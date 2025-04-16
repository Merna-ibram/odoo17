{
    'name': "TO_DA APP",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'views/todo_task_line_view.xml'
    ],


    'application': True,

}