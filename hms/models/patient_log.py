from odoo import models, fields


class LogHistory(models.Model):
    _name = "log.history"

    created_by = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)
    created_date = fields.Date()
    description = fields.Text()

    patient_id = fields.Many2one(comodel_name="hms.patient")