from odoo import models, fields

class PropertyChangeState(models.TransientModel):
    _name = 'property_change_state'

    property_id = fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
    ], default='draft')
    reason = fields.Char()   

    def action_confirm(self):
        if self.property_id.state == "closed":
            self.property_id.state = self.state
            self.property_id.create_history_record ('closed' , self.state , self.reason)