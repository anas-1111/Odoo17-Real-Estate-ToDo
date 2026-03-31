from odoo import api, models, fields

class Tag(models.Model):
    _name = 'tag'

    name = fields.Char(string="Name", required=True)