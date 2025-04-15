from odoo import models, fields

class Tags(models.Model):
    _name = 'tags'
    _description = "Tags Information"

    name = fields.Char(required=True)
    property_ids = fields.Many2many('property')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name already exists! Please try another one.')
    ]
