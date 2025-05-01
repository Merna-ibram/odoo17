from odoo import models, fields, api


class ToDoListLine(models.Model):
    _name = 'todo.list.line'
    _description = "To-Do List Line"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    task_id = fields.Many2one('todo.list', string="Task")
    description = fields.Text()
    time_spent = fields.Float(string="Time Spent (hrs)")


    def check_total_time(self):
        """Check if this line's task has exceeded its estimated time.

        Returns:
            str: A message indicating whether the time limit was exceeded.
        """
        task = self.task_id
        if not task or not task.estimated_time:
            total_time = sum(task.task_line_ids.mapped('time_spent'))
            return f"Time logged: {total_time:.2f} hrs (no estimate set)"

        total_time = sum(task.task_line_ids.mapped('time_spent'))
        if total_time > task.estimated_time:
            return f"Exceeds by {total_time - task.estimated_time:.2f} hrs"
        else:
            return "Within estimate"