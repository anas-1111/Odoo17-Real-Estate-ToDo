from email.policy import default

from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError

class Todo(models.Model):
    _name = 'todo'
    _description = 'ToDo'

    ref = fields.Char(string="Reference", default="Task", readonly=True)
    name = fields.Char(string='Task', required=True)
    assigned_to = fields.Many2one(comodel_name='res.partner', string='Assigned To', required=True)
    description = fields.Text(string='Description', required=True)
    due_date = fields.Date(string='Due Date', required=True)
    status = fields.Selection([
        ('new', 'New'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ], default='new', string='Status')
    estimated_time = fields.Integer(string='Estimated Time')
    line_ids = fields.One2many(comodel_name='todo.line', inverse_name='todo_id')
    active = fields.Boolean(default=True)
    is_late = fields.Boolean(string="Is late", default=False)

    def action_in_progress(self):
        for rec in self:
            rec.status = "in progress"

    def action_completed(self):
        for rec in self:
            rec.status = "completed"

    def action_closed(self):
        for rec in self:
            rec.status = "closed"

    def check_due_date(self):
        todo_ids = self.search([])
        for rec in todo_ids:
            if rec.status in ['new', 'in progress']:
                if rec.due_date and rec.due_date < fields.Date.today():
                    rec.is_late = True

    @api.model
    def create(self, vals):
        res = super(Todo, self).create(vals)
        if res.ref == 'Task':
            res.ref = self.env['ir.sequence'].next_by_code('task_seq')
        return res

    def action_open_change_assign_wizard(self):
        action = self.env.ref('to_do.change_assign_wizard_action').read()[0]
        action['context'] = {
            'active_model': 'todo',
            'active_ids': self.ids,
        }
        return action


class ToDoLines(models.Model):
    _name = 'todo.line'


    time = fields.Integer(string="Time")
    description = fields.Text(string="Description")
    todo_id = fields.Many2one(comodel_name="todo", string="ToDo")

    @api.constrains('time', 'todo_id')
    def _check_total_time(self):
        for rec in self:
            if rec.todo_id:
                total = sum(line.time for line in rec.todo_id.line_ids)
                if total > rec.todo_id.estimated_time:
                    raise ValidationError("Total time exceeds estimated time")

