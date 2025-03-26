from odoo import models, fields, api


class Owner(models.Model):
    _name = 'owner'
    _description = "Owner Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name =  fields.Char(required=True , tracking=1)
    phone_number = fields.Char(required=True, size=12 , tracking=1)
    address = fields.Char()
    e_mail = fields.Char()

    property_ids = fields.One2many('property', 'owner_id')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'this name is exist ! please try anther one')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Owner, self).create(vals_list)
        print("inside create method")
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Owner, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("inside search method")
        return res

    def write(self, vals_list):
        res = super(Owner, self).write(vals_list)
        print("inside write method")
        return res

    def unlink(self):
        res = super(Owner, self).unlink()
        print("inside deleted method")
        return res
