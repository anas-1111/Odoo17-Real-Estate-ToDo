from odoo import api, models, fields

class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(string="Name", required=True)
    phone = fields.Char(string="Phone")
    address = fields.Char(string="Address")

    property_ids = fields.One2many(comodel_name='property', inverse_name='owner_id', string="Properties")