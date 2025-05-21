from odoo import models, fields

class ToDoAssignmentWizard(models.TransientModel):
    _name = 'todo_assignment'
    _description = 'Bulk Task Assignment Wizard'

    employee_id = fields.Many2one('res.users', string='Assign To', required=True)
    task_ids = fields.Many2many('todo.list', string='Tasks')

    def assign_tasks(self):
        for task in self.task_ids:
            task.assign_to = self.employee_id
