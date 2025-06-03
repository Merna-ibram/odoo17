from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'invoices'

    date = fields.Date(related='partner_id.date', string="Subscription start date", readonly=True)
    months = fields.Integer(related='partner_id.months', string="Months of subscription")
    end_date = fields.Date(related='partner_id.end_date', string="Subscription End Date", readonly=True)
    code = fields.Char(related='partner_id.code', readonly=1, string="Code")
    age = fields.Integer(related='partner_id.age',string="Age")
    gender = fields.Selection(related='partner_id.gender', string="Gender")

