from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PROPERTY(models.Model):
    _name = 'property'
    _description = "Property Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='new', readonly=1)
    name = fields.Char(required=True, size=15, translate=True)
    active = fields.Boolean(default=1)
    property_image = fields.Image()
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float(digits=(0, 2), tracking=1)
    selling_price = fields.Float(digits=(0, 2), tracking=1)
    diff = fields.Float(compute='_compute_diff', store=1)
    bedrooms = fields.Integer(tracking=1)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'NORTH'),
        ('south', 'SOUTH'),
        ('east', 'EAST'),
        ('west', 'WEST'),
    ], default='north')
    owner_id = fields.Many2one('owner')
    tags_id = fields.Many2many('tags')
    line_ids = fields.One2many('property_line', 'property_id')
    living_area_ids = fields.One2many('property_line2', 'living_area_id')
    owner_address = fields.Char(related='owner_id.address', readonly=0, store=1)
    owner_phone_number = fields.Char(related='owner_id.phone_number')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold_out', 'Sold_out'),
        ('closed', 'Closed'),
    ], default='draft')

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('please add valid number of bedrooms')

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'


    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold_out(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold_out')
            rec.state = 'sold_out'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'


    def action_open_state(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.property_change_state_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    @api.model
    def create(self, vals):

        res = super(PROPERTY, self).create(vals)

        # After creation, if the reference is still the default 'new',
        # generate the next sequence number
        if res.ref == 'new':
            sequence = self.env['ir.sequence'].next_by_code('property_seq')
            if sequence:
                # Update the record with the generated sequence
                res.ref = sequence

        return res

    @api.model
    def check_expected_date(self):
        print(self)
        property_ids = self.search([])
        print(property_ids)
        for rec in property_ids:
            print(rec)
            if rec.expected_date and rec.expected_date < fields.date.today():
                rec.is_late = True

    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.expected_price < 0:
                return {
                    'warning': {
                        'title': 'Warning',
                        'message': 'Expected price should not be negative.',
                        'type': 'notification'
                    }
                }

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'this name is exist ! please try anther one')
    ]

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(PROPERTY, self).create(vals_list)
    #     print("inside create method")
    #     return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(PROPERTY, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("inside search method")
        return res

    def write(self, vals_list):
        res = super(PROPERTY, self).write(vals_list)
        print("inside write method")
        return res

    def unlink(self):
        res = super(PROPERTY, self).unlink()
        print("inside deleted method")
        return res

    def action(self):
        # print(self.env.user.name)
        # print(self.env.user.login)
        # print(self.env.user.id)
        # print(self.env.company.name)
        # print(self.env.company.id)
        # print(self.env.company.street)
        # print(self.env.context)
        # print(self.env.cr)
        # print(self.env['owner'].create({
        #     'name': '5458',
        #     'address': 'maghagha',
        #     'e_mail': 'sfdsfvds',
        #     'phone_number': '0236564415631'
        # }))
        print(self.env['property'].search([('name','!=','property')]))

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description' : line.description, 'area' : line.area})for line in rec.line_ids],
            })


class PROPERTYLine(models.Model):
    _name = 'property_line'
    _description = "Property Line"

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
    room_image = fields.Image()


class PROPERTYLine2(models.Model):
    _name = 'property_line2'
    _description = "Property Line"

    living_area_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
    room_image = fields.Image()

