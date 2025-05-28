from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_image = fields.Image(string="Product Image",  related='product_id.image_128', store=False)

    # @api.depends('product_id')
    # def _compute_product_image(self):
    #     show_image = self.env['ir.config_parameter'].sudo().get_param(
    #         'sale_product_image.show_product_image_in_order_line', default=False)
    #     for line in self:
    #         if show_image and line.product_id.image_128:
    #             line.product_image = line.product_id.image_128
    #         else:
    #             line.product_image = False
