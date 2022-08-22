from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(Http, self).session_info()
        user = request.env.user
        res.update({
            'group_export_data': user and user.has_group('web_disable_action.group_export_data'),
            'group_archive_data': user and user.has_group('web_disable_action.group_archive_data'),
        })
        return res
