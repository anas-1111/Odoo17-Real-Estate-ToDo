from odoo import api, models, fields

# New Model But from Other Model And Create New Table But With The Same Fields (2nd Type)

class Client(models.Model):
    _name = 'client'
    _inherit = 'owner'

