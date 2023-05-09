from odoo import fields, models, api
from odoo.tools.safe_eval import safe_eval


class PlayGround(models.Model):

    _name = 'play.ground'
    _description = 'Play Ground'

    DEFAULT_ENV_VARIABLES = """# Available variables
    # self: Current object
    # self.env: Odoo Environment on which the action is triggered
    # self.env.user: Return the whether the current user has a group "setting", or is in super user mode.
    # self.env.is_system: Return the whether the current user has a group "Access rights", or is in super user mode.
    # self.env.is_superuser: Return the whether the environment is in superuser mode.
    # self.env.company: Return the current company (as in instance)
    # self.env.companies: Return the recordset of the enabled companies by the user
    # self.env.lang: Return the current language code
    # self.env.cr: Curser
    # self.env.context: Context
    """

    model_id = fields.Many2one('ir.model',string="Model")
    code = fields.Text(string="Code", default=DEFAULT_ENV_VARIABLES)
    result = fields.Text(string="Result")

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            self.result = safe_eval(self.code.strip(), {'self': model})
        except Exception as e:
            self.result = str(e)
