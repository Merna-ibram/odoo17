from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property', string="Property")

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        print("Inside action_confirm method")
        return res
