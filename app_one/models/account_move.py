from odoo import models , fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_id = fields.Many2one('property')



    def action_do_something(self):
        print(self, "inside action do something method")

