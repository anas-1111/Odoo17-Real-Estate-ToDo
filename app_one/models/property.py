from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import ValidationError
import requests

class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(string="Reference", default='New', readonly=True)
    name = fields.Char(string="Name", required=True, default='New Property')
    description = fields.Text(string="Description", tracking=True)
    postcode = fields.Char(string="Postcode", required=True)
    date_availability = fields.Date(string="Date Availability", tracking=True)
    expected_selling_date = fields.Date(string="Expected Selling Date", tracking=True)
    is_late = fields.Boolean(string="Is late")
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price")
    diff = fields.Float(string="Difference", compute="_compute_diff", store=True)
    bedrooms = fields.Integer(string="Bedrooms", required=True)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West")
    ], default="north", string="Garden Orientation")
    owner_id = fields.Many2one(comodel_name="owner", required=True, string="Owner")
    tag_ids = fields.Many2many(comodel_name="tag", string="Tags")
    owner_address = fields.Char(string="Owner Address", related="owner_id.address") # readonly = 1, store = 1
    owner_phone = fields.Char(string="Owner Phone", related="owner_id.phone")
    create_time = fields.Datetime(string="Create Time", default=fields.Datetime.now())
    next_time = fields.Datetime(string='Next Time', compute='_compute_next_time')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("sold", "Sold"),
        ("closed", "Closed")
    ], default="draft", string="State")

    line_ids = fields.One2many(comodel_name="property.line", inverse_name="property_id")

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'Name is Exist!')
    ]

    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False


    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            # print(rec)
            # print("Inside _compute_diff")
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('living_area')
    def _onchange_living_area(self):
        for rec in self:
            if rec.living_area < 0:
                return {
                    'warning':{'title':'Warning', 'message':'Negative Value', 'type':'notifcation'}
                }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError("Bedrooms must be greater than zero")

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = "draft"
            # rec.write({
            #     'state': 'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.write({'state': 'pending'})

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = "sold"

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = "closed"

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.state in ['draft', 'pending']:
                if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                    rec.is_late = True

    def action(self):
        #[('name', '=', 'property 1')]
        print(self.env['property'].search([('name', '=', 'Property 1')]))

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id' : rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {
                    'description': line.description,
                    'area': line.area
                }) for line in rec.line_ids]
            })

    def action_open_change_state_wizard(self):
        action = self.env.ref('app_one.change_state_wizard_action').read()[0]
        action['context'] = {
            'active_model': 'property',
            'active_ids': self.ids,
        }
        return action

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    def get_properties(self):
        payload = dict()
        response = requests.get('http://anas-hp-laptop-15-da2xxx:8069/v1/list-property', data=payload)
        print(response.content)

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(Property, self).create(vals_list)
    #     print("Inside")
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("Inside")
    #     return res
    #
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("Inside")
    #     return res
    #
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("Inside")
    #     return res


class PropertyLines(models.Model):
    _name = 'property.line'


    area = fields.Float(string="Area")
    description = fields.Text(string="Description")
    property_id = fields.Many2one(comodel_name="property", string="Property")