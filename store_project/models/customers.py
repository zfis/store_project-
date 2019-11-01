from odoo import models, fields, api

class StoreProjectCustomersFormInherit(models.Model):
    _inherit = 'res.partner'
    # _order = 'summation desc'

    fname = fields.Char(string="First Name")
    lname = fields.Char(string="Last Name")
    name = fields.Char(compute="_compute_total_name", store='True', readonly='False')
    mobile = fields.Char(default='01')

    internal_ref = fields.Char(string='Internal Reference')
    additional_notes = fields.Text(string="Notes")

    refs = fields.Many2many(comodel_name="res.partner", string='References',relation="minitracks", column1="refs",
                            culomn2="refs_ids")
    refs_ids = fields.Many2many(comodel_name="res.partner", string='References', relation="minitracks", column1="refs_ids",
                                culomn2="refs")

    summation = fields.Integer(string='References Number', compute='_compute_refs')


    _sql_constraints = [
        ('customer_mobile_uniqe', 'unique (mobile)', 'The mobile of the customer already exists it  must be unique  !')
    ]



    @api.one
    @api.depends('fname', 'lname')
    def _compute_total_name(self):
        if self.fname and self.lname :
            self.name = (str(self.fname) + " " +str(self.lname))
        elif self.fname:
            self.name = self.fname
        elif self.lname:
            self.name = self.lname
        else:
            self.name = ""



    @api.multi
    @api.onchange('refs')
    def _compute_refs(self):
        for partner in self:
            partner.summation = len(partner.refs)
