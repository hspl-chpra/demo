from odoo import fields, models, api
# from odoo.tool.safe_eval import safe_eval


class PlayGround(models.Model):

    _name = 'play.ground'
    _description = 'Play Ground'

    DEFAULT_ENV_VARIABLES = """# Available variables
    # self: Current object
    # self.env: Odoo Environment on which the action is triggered
    # self.env.user: Return the whether the current user has a group "setting", or is in super user mode.
    """

    model_id = fields.Many2one('ir.model',string="Model")
    code = fields.Text(string="Code", default=DEFAULT_ENV_VARIABLES)
    result = fields.Text(string="Result")

    def action_execute(self):
        pass
