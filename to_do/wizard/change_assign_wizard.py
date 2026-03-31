from odoo import api, fields, models


class ChangeAssign(models.TransientModel):
    _name = 'change.assign'

    task_id = fields.Many2one('todo')
    assigned_to = fields.Many2one(comodel_name='res.partner', string='Assigned To', required=True)
    reason = fields.Char(string='Reason')

    def action_confirm(self):
        task_ids = self.env['todo'].browse(self.env.context.get('active_ids', []))
        for task_id in task_ids:
            if task_id.status in ['new', 'in progress']:
                task_id.assigned_to = self.assigned_to
            else:
                continue
