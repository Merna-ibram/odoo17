from odoo import models, fields

class ToDoListLine(models.Model):
    _name = 'todo.list.line'
    _description = "To-Do List Line"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    task_id = fields.Many2one('todo.list', string="Task")
    description = fields.Text()
    time_spent = fields.Float(string="Time Spent (hrs)")

