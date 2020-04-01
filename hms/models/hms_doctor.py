from odoo import fields, models

class HmsDoctor(models.Model):
    _name = "hms.doctor"
    _rec_name = "first_name"
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Binary()

    department_id = fields.Many2one(comodel_name="hms.department")



