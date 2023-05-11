from odoo import fields, models, api


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False

    operations_name = fields.Char(string="Name")
    doctor_id = fields.Many2one('res.users', string="Doctor")
    reference_record = fields.Reference(selection=[('hospital.patient', 'Patient'), ('hospital.appointment', 'Appointment')], string="Record")

    @api.model
    def name_create(self, name):
        print("..................", name)
        return self.create({'operations_name': name}).name_get()[0]