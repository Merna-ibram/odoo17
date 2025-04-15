from odoo import models, fields, api


class Client(models.Model):
    _name = 'client'
    _inherit = 'owner'
    _description = 'Client Model'

    phone_number2 = fields.Char(required=True, size=12)

    _sql_constraints = [
        ('phone_length_check', 'CHECK (char_length(phone_number2) = 12)',
         'Phone number must be exactly 12 characters long.')
        ]