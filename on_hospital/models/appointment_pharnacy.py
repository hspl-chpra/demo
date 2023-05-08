from odoo import fields, models, api


class AppointmentPharmacy(models.Model):

    _name = 'appointment.pharmacy'
    _description = 'Appointment Pharmacy'

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
