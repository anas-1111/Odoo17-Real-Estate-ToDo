from odoo import api, fields, models


class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending')
    ], default='draft')
    reason = fields.Char(string='Reason')

    def action_confirm(self):
        property_ids = self.env['property'].browse(self.env.context.get('active_ids', []))
        for property_id in property_ids:
            old_state = property_id.state
            property_id.state = self.state
            property_id.create_history_record(old_state, self.state, self.reason)
