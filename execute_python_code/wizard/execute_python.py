from odoo import models, fields
from odoo.exceptions import Warning


class ExecutePython(models.Model):
    _name = "execute.python"
    _description = "Execute Python Code"

    name = fields.Char(string='Name', size=1024, required=True)
    code = fields.Text(string='Python Code', required=True)
    result = fields.Text(string='Result', readonly=True)

    def execute_code(self):
        localdict = {'self': self}
        for obj in self:
            try:
                exec(obj.code, localdict)
                if localdict.get('result', False):
                    self.write({'result': localdict['result']})
                else:
                    self.write({'result': ''})
            except Exception as e:
                raise Warning('Python code is not able to run ! message : %s' % (e))

        return True

    def offer_timing_updation(self):
        rec = self.search([('name', '=', 'Update Offer Timing')])
        if rec:
            rec.execute_code()
