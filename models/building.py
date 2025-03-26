from odoo import models, fields

class Building(models.Model):
    _name = 'building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'no'
    _description = 'Building Model'


    name = fields.Char()
    active = fields.Boolean(default=True)
    no = fields.Integer()
    description = fields.Text()
    code = fields.Char(required=True)
    date_availability = fields.Date(tracking=True)

