# -*- coding: utf-8 -*-

from odoo.http import route, request
from odoo.addons.mass_mailing.controllers.main import MassMailController


class MassMailController(MassMailController):

    @route('/website_mass_mailing/get_google_recaptcha_key', type='json', website=True, auth="public")
    def get_recaptcha_key(self, **post):
        Website = request.env['website']
        Website = Website.get_current_website()
        return {'recaptcha_key': Website.recaptcha_key_site}

    @route('/website_mass_mailing/subscribe', type='json', website=True, auth="public")
    def subscribe(self, list_id, email, **post):
        # Override this method to add name in mailing contact.
        ContactSubscription = request.env['mailing.contact.subscription'].sudo()
        Contacts = request.env['mailing.contact'].sudo()
        name, email = Contacts.get_name_email(email)
        if name == email and post.get('cust_name', False):
            name = post.get('cust_name')

        subscription = ContactSubscription.search([('list_id', '=', int(list_id)), ('contact_id.email', '=', email)], limit=1)
        if not subscription:
            # inline add_to_list as we've already called half of it
            contact_id = Contacts.search([('email', '=', email)], limit=1)
            if not contact_id:
                contact_id = Contacts.create({'name': name, 'email': email})
            ContactSubscription.create({'contact_id': contact_id.id, 'list_id': int(list_id)})
        elif subscription.opt_out:
            subscription.opt_out = False
        # add email to session
        request.session['mass_mailing_email'] = email
        mass_mailing_list = request.env['mailing.list'].sudo().browse(list_id)

        if mass_mailing_list.send_subscribe_mail:
            email_values = {
                'email_to': contact_id and contact_id.email
            }
            mass_mailing_list.template_id.send_mail(contact_id.id, force_send=True, email_values=email_values)
        return {'toast_content': mass_mailing_list.toast_content}
