from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ToDoList(models.Model):
    _name = 'todo.list'
    _description = "To-Do List Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    task_name = fields.Char(required=True)
    assign_to = fields.Many2one('res.users')
    description = fields.Text()
    due_date = fields.Date()
    expected_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    state = fields.Selection([
        ('new', 'New'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ], default='new')
    active = fields.Boolean(default=True)
    estimated_time = fields.Float(string="Estimated Time (hrs)")
    task_line_ids = fields.One2many("todo.list.line", "task_id", string="Timesheet Lines")

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
        print("Closing task...")
        for rec in self:
            rec.state = 'closed'

    @api.model
    def check_expected_date(self):
        print(self)
        task_name = self.search([])
        print(task_name)
        for rec in task_name:
            print(rec)
            if rec.expected_date and rec.expected_date < fields.date.today():
                rec.is_late = True

    @api.constrains('task_line_ids', 'estimated_time')
    def _check_total_time(self):
        for rec in self:
            total_time = sum(rec.task_line_ids.mapped('time_spent'))
            if rec.estimated_time and total_time > rec.estimated_time:
                raise ValidationError("Total time spent exceeds estimated time!")
