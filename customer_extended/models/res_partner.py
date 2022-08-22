import base64
from odoo import models, fields, _


class Partner(models.Model):
    _inherit = 'res.partner'

    auto_send_statement = fields.Boolean(string="Auto Send Statement")

    def auto_generate_and_send_statement_to_partner(self):
        account_partner_ledger_obj = self.env['account.partner.ledger']
        partners = self.env['res.partner'].search([('auto_send_statement', '=', True)])
        for partner in partners:
            partner_ledger_data = account_partner_ledger_obj.with_context(auto_send_statement=True).get_report_informations({'partner_ids': [partner.id]})
            partner_ledger_data.get('options').update({'unfold_all': True})
            get_pdf_data = account_partner_ledger_obj.get_pdf(partner_ledger_data.get('options'))
            mail_compose_message_data = partner.create_mail_wizard(get_pdf_data)
            if mail_compose_message_data:
                mail_compose_message_data.action_send_mail()
        return True

    def create_mail_wizard(self, pdf_data):
        mail_compose_message_obj = self.env['mail.compose.message']
        attachment = self.env['ir.attachment'].create({
            'name': "Customer Statement.pdf",
            'type': 'binary',
            'datas': base64.b64encode(pdf_data),
            'description': 'Customer Statement',
            'res_model': self._name,
            'res_id': self.id
        })
        mail_compose_message = mail_compose_message_obj.create({
            'subject': 'Customer Statement',
            'body': '',
            'partner_ids': [partner.id for partner in self],
            'attachment_ids': [(4, attachment.id)],
            'email_from': self.email or False,
        })
        return mail_compose_message
