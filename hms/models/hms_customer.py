from odoo import fields, models, api
from odoo.exceptions import UserError

class CustomerInherit(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one(comodel_name="hms.patient")
    vat = fields.Char(required=True)
    # @api.model
    # def create(self, vals):
    #     patients = self.env['hms.patient'].search([('email', '=', vals.get('email'))])
    #     for record in patients:
    #         if record.id:
    #             raise UserError("This email already exist")
    #         else:
    #             new_customer = super().create(vals)
    #             return new_customer

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise UserError("You can't delete this customer")
        super().unlink()

