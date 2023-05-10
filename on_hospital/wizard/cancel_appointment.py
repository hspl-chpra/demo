from odoo import fields, models, api, _
import datetime
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):

    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        # print("Default get executed", res)
        # print(".......context", self.env.context.get('active_id'))
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment", domain=['|', ('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date("Cancellation date")

    def action_cancel(self):
        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError(_("Sorry! You are not allowed to cancel"))
        self.appointment_id.state = 'cancel'
        return
