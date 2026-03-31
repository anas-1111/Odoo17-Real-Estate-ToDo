from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    # price = fields.Float(string="Price", compute="_compute_price", store=True)
    property_id = fields.Many2one(string="Property", comodel_name='property')
    price = fields.Float(string="Price", related="property_id.selling_price")

    # @api.depends('property_id')
    # def _compute_price(self):
    #     for rec in self:
    #         rec.price = rec.property_id.selling_price