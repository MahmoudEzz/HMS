from odoo import fields, models, api
from datetime import datetime, date
import re
from odoo.exceptions import UserError


class HmsPatient(models.Model):
    _name = "hms.patient"

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    email = fields.Char()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+')])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute="compute_age", store=True)
    state = fields.Selection([('undetermined', 'Undetermined'),
                              ('good', 'Good'),
                              ('fair', 'Fair'),
                              ('serious', 'Serious')
                              ], default="undetermined")

    department_id = fields.Many2one(comodel_name="hms.department")
    doctors_ids = fields.Many2many(comodel_name="hms.doctor")

    log_ids = fields.One2many(comodel_name="log.history", inverse_name="patient_id")

    department_capacity = fields.Integer(related="department_id.capacity")

    @api.onchange("age")
    def onchange_age(self):
        if self.age < 30 and self.age:
            self.pcr = True
            return {
                'warning': {'title': "Warning",
                            'message': "PCR has been checked"}
            }
        else:
            self.pcr = False

    @api.multi
    def change_state(self):
        if not self.state:
            self.state = 'undetermined'
        elif self.state == 'undetermined':
            self.state = 'good'
        elif self.state == 'good':
            self.state = 'fair'
        elif self.state == 'fair':
            self.state = 'serious'
        else:
            self.state = 'undetermined'
        result = self.env['log.history'].create({
                'created_date': datetime.now(),
                'description': f"updated to {self.state}",
                'patient_id': self.id
            })
        return result


# lab 2 field

    # @api.model
    # def create(self, vals):
    #     email = vals.get('email')
    #     regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    #     if re.search(regex, email):
    #         res = self.search([('email', '=', email)])
    #         if res.id:
    #             raise UserError("This email already exist")
    #         else:
    #             patient = super().create(vals)
    #             return patient
    #     else:
    #         raise UserError("Invalid Email Address")

    @api.constrains('email')
    def check_email(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex, self.email):
            return
        else:
            raise UserError("Invalid Email Address")
    _sql_constraints = [
        ('validate email', 'UNIQUE(email)', 'This email already exist')
    ]

    @api.depends('birth_date')
    def compute_age(self):
        for record in self:
            if record.birth_date is not False:
                today = date.today()
                record.age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))



