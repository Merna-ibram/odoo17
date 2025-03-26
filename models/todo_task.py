from odoo import models, fields

class ToDoList(models.Model):
    _name = 'todo.list'
    _description = "To-Do List Information"

    task_name = fields.Char(required=True)
    assign_to = fields.Many2one('res.users')
    description = fields.Text()
    due_date = fields.Date()
    state = fields.Selection([
        ('new', 'New'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='new')

    def action_do(self):
        self.state = 'new'

    def action_doing(self):
        self.state = 'in progress'

    def action_done(self):
        self.state = 'completed'

