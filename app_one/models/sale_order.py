from odoo import api, fields, models, exceptions

# To Edit Function Or Method From Model And To Connect To Models Or Add Feature To The Model (1st Type)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one(comodel_name='property',string="Property") # Type 1 Inheritance

    def action_confirm(self): # Python Inheritance
        res = super(SaleOrder, self).action_confirm()
        print("Inside action_confirm method")
        return res