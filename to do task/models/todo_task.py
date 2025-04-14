from odoo import models, fields

class ToDoList(models.Model):
    _name = 'todo.list'
    _description = "To-Do List Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    task_name = fields.Char(required=True)
    assign_to = fields.Many2one('res.users')
    description = fields.Text()
    due_date = fields.Date()
    state = fields.Selection([
        ('new', 'New'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ], default='new')
    active = fields.Boolean(default=True)
    estimated_time = fields.Float(string="Estimated Time (hrs)")
    task_line_ids = fields.One2many("todo.task.line", "task_id", string="Timesheet Lines")
    line_ids = fields.One2many('todo_line', 'task_id')

    def action_new(self):
        for rec in self:
            rec.state = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in progress'

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'



