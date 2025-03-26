from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

#    price = fields.Float(compute='_compute_price', store=True)
    property_id = fields.Many2one('property')
    price = fields.Float(related='property_id.selling_price')
    assign_id = fields.Many2one('todo.list')
    assign_to = fields.Many2one('res.partner', related='assign_id.assign_to')
#
#    @api.depends('property_id')
#    def _compute_price(self):
#        for rec in self:
#            rec.price = rec.property_id.selling_price

