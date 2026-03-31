from odoo import api, fields, models, exceptions

class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property History'

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one(comodel_name='property')
    old_state = fields.Char('Old State')
    new_state = fields.Char('New State')
    reason = fields.Char('Reason')
    line_ids = fields.One2many(comodel_name='property.history.line', inverse_name='history_id')

class PropertyHistoryLine(models.Model):
    _name = 'property.history.line'

    area = fields.Float(string="Area")
    description = fields.Text(string="Description")
    history_id = fields.Many2one(comodel_name="property.history", string="Property")