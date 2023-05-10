from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient', string="Patient", ondelete="restrict")
    gender = fields.Selection(related='patient_id.gender')
    ref = fields.Char(string="Reference", default="Odoo", help='Reference of the patient from patient records')
    appointment_time = fields.Datetime(string="Appointment Time",  default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft', string="Status", required=True)
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=True)
    pharmacy_ids = fields.One2many('appointment.pharmacy','appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string="Hide sales prices")

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("You can only  delete 'draft' state"))
        return super(HospitalAppointment, self).unlink()

    def acton_done(self):
        print("Button clicked........")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successfull',
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'in_consultation'

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_done(self):
        for record in self:
            record.state = 'done'



