import werkzeug.urls
from odoo import models


class Partner(models.Model):
    _inherit = "res.partner"

    def google_map_link(self, zoom=10):
        params = {
            'q': '%s, %s %s, %s' % (self.street or '', self.city or '', self.zip or '', self.country_id and self.country_id.display_name or ''),
            'z': zoom,
            'output': 'classic',
        }
        return 'https://maps.google.com/maps?' + werkzeug.urls.url_encode(params)
