from odoo import fields,models,api
from odoo.exceptions import ValidationError

class TaskLine(models.Model):
    _name = "todo.task.line"
    _description = "Task Timesheet Line"

    task_id = fields.Many2one("todo.task", string="Task")
    user_id = fields.Many2one("res.users", string="User")
    time_spent = fields.Float(string="Time Spent (hrs)")

    @api.constrains('task_line_ids')
    def _check_total_time(self):
        for task in self:
            total = sum(task.task_line_ids.mapped('time_spent'))
            if total > task.estimated_time:
                raise ValidationError("Total time spent exceeds estimated time!")
