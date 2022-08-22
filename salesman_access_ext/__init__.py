# -*- coding: utf-8 -*-

from . import models
from odoo import api, SUPERUSER_ID


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Revert back to default access settings on uninstall.
    env.ref('crm.access_res_partner').write({'perm_create': True, 'perm_write': True})

    env.ref('base.res_partner_rule').write({'groups': False})
    env.ref('base.res_partner_rule_private_employee').write(
        {'domain_force': "['|', ('type', '!=', 'private'), ('type', '=', False)]"})
    env.ref('sale.sale_order_line_personal_rule').write(
        {'domain_force': "['|',('salesman_id','=',user.id),('salesman_id','=',False)]"})
    env.ref('sale.sale_order_report_personal_rule').write(
        {'domain_force': "['|',('user_id','=',user.id),('user_id','=',False)]"})
    env.ref('sale.account_invoice_line_rule_see_personal').write(
        {
            'domain_force': "[('move_id.type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')), '|', ('move_id.invoice_user_id', '=', user.id), ('move_id.invoice_user_id', '=', False)]"})
    env.ref('sale.account_invoice_report_rule_see_personal').write(
        {'domain_force': "['|', ('invoice_user_id', '=', user.id), ('invoice_user_id', '=', False)]"})
    env.ref('sale.sale_order_personal_rule').write(
        {'domain_force': "['|',('user_id','=',user.id),('user_id','=',False)]"})
    env.ref('sale.account_invoice_rule_see_personal').write(
        {'domain_force': "[('type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')), '|', ('invoice_user_id', '=', user.id), ('invoice_user_id', '=', False)]"})
    env.ref('crm.crm_activity_report_rule_personal_activities').write(
        {'domain_force': "['|',('user_id','=',user.id),('user_id','=',False)]"})
    env.ref('crm.crm_rule_personal_lead').write(
        {'domain_force': "['|',('user_id','=',user.id),('user_id','=',False)]"})
