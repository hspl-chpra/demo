from odoo import fields, models, api, _


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True, copy=False)
    color = fields.Integer(string="Color")
    color2 = fields.Char(string="Color2")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        if not default.get('name'):
            default['name'] = _("%s (Copy)", self.name)

        default['sequence'] = 10
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'A reconciliation model already bears this name.'),
        ('check_sequence', 'check (sequence > 0)', 'Sequence must be non zero')
    ]
