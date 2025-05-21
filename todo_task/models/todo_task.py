
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute
from datetime import  timedelta

class ToDoList(models.Model):
    _name = 'todo.list'
    _description = "To-Do List Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='new', readonly=1)
    name = fields.Char(required=True, string='Task Name', translate=True)
    assign_to = fields.Many2one('res.users', ondelete='set null')
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
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='compute_next_time')
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
        name = self.search([])
        print(name)
        for rec in name:
            print(rec)
            if rec.expected_date and rec.expected_date < fields.date.today():
                rec.is_late = True

    def action(self):
        print(self.env.user.name)
        print(self.env.user.login)
        print(self.env.user.id)
        print(self.env.company.name)
        print(self.env.company.id)
        print(self.env.company.street)
        print(self.env.context)
        print(self.env.cr)

    @api.model
    def create(self, vals):
        res = super(ToDoList, self).create(vals)
        if res.ref == 'new':
            sequence = self.env['ir.sequence'].next_by_code('todo_list_seq')
            if sequence:
                res.ref = sequence

        return res


    def create_new_line(self, description,time_spent):
          for rec in self:
            rec.env['todo.list.line'].create({
                'task_id': rec.id,
                'description': description,
                'time_spent': time_spent,
            })
          print(self.env['todo.list.line'].search([]))

    @api.constrains('task_line_ids', 'estimated_time')
    def _check_total_time(self):
        for rec in self:
            total_time = sum(rec.task_line_ids.mapped('time_spent'))
            if rec.estimated_time and total_time > rec.estimated_time:
                raise ValidationError("Total time spent exceeds estimated time!")

    @api.depends('create_time')
    def compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time =  rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False