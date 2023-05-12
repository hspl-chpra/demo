from datetime import date
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital patient'

    name = fields.Char(string="Name", tracking=True)
    age = fields.Integer(string="Age", tracking=True, compute="_compute_age", inverse="_inverse_age", search="search_age", store=True)
    date_of_birth = fields.Date(string="Date Of Birth", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'female')], string="Gender", tracking=True, default='female')
    ref = fields.Char(string="Reference", default="Odoo")
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointments")
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    appointment_count = fields.Integer(string="Appointment Counter", compute="_compute_appointment_count", store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status", tracking=True)
    partner_name = fields.Char(string="Partner name")
    is_birthday = fields.Boolean(string='Birthday ?', compute="_compute_is_birthday")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique')
    ]

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date is not acceptable"))

    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for record in self:
            if record.appointment_ids:
                raise ValidationError("you can not delete a patient with appointment")

    @api.model
    def create(self, vals):
        # print("..............",self.env['ir.sequence'])
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        # print("Write method is triggered..", vals)
        if not self.ref and not vals.get['ref']:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')

        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        # print("today", today)
        # print("self.date_of_birth", self.date_of_birth, self.date_of_birth.year)
        if self.date_of_birth:
            self.age = today.year - self.date_of_birth.year
        else:
            self.age = 0

    @api.depends('age')
    def _inverse_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def search_age(self, operator, value):
        date_of_birth =  date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', ' >=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    def name_get(self):
        # patient_list = []
        # for record in self:
        #     name = record.ref + ' ' + record.name
        #     patient_list.append((record.id, name))
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]

    def action_test(self):
        print("Clicked")
        return

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                print("Today............", today)
                print("Birth date............", rec.date_of_birth.day)
                print("Birth month............", rec.date_of_birth.month)
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday
