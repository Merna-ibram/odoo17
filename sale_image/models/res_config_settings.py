from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_product_image = fields.Boolean(string="Show Product Image in Sale Report", config_parameter='sale_product_image.show_product_image')