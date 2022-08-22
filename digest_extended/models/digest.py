import logging
from datetime import date
from odoo.exceptions import AccessError
from odoo import fields, models, tools, _
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class Digest(models.Model):
    _inherit = 'digest.digest'

    periodicity = fields.Selection(selection_add=[('daily', 'Daily')])

    def _get_next_run_date(self):
        self.ensure_one()
        if self.periodicity == 'daily':
            delta = relativedelta(days=1)
        if self.periodicity == 'weekly':
            delta = relativedelta(weeks=1)
        elif self.periodicity == 'monthly':
            delta = relativedelta(months=1)
        elif self.periodicity == 'quarterly':
            delta = relativedelta(months=3)
        return date.today() + delta

    kpi_takealot_capetown = fields.Boolean('Capetown Sales')
    kpi_takealot_capetown_value = fields.Monetary(compute='_compute_kpi_takealot_capetown_value')
    kpi_takealot_johannesburg = fields.Boolean('Johannesburg Sales')
    kpi_takealot_johannesburg_value = fields.Monetary(compute='_compute_kpi_takealot_johannesburg_value')

    kpi_takealot_capetown_count = fields.Boolean('Capetown Sales Count')
    kpi_takealot_capetown_count_value = fields.Integer(compute='_compute_kpi_takealot_capetown_count_value')
    kpi_takealot_johannesburg_count = fields.Boolean('Johannesburg Sales Count')
    kpi_takealot_johannesburg_count_value = fields.Integer(compute='_compute_kpi_takealot_johannesburg_count_value')

    kpi_ecommerce_trending_product = fields.Boolean('eCommerce Trending Product')
    kpi_ecommerce_trending_product_value = fields.Many2many('product.product', 'ecommerce_product_digest_rel_ts', 'digest_id', 'product_id', string='eCommerce Trending Products Values',
                                                            compute='_kpi_ecommerce_trending_product_value')

    kpi_pos_trending_product = fields.Boolean('PoS Trending Product')
    kpi_pos_trending_product_value = fields.Many2many('product.product', 'pos_product_digest_rel_ts', 'digest_id', 'product_id', string='PoS Trending Products Values',
                                                      compute='_kpi_pos_trending_product_value')

    kpi_sale_trending_product = fields.Boolean('Wholesale Trending Product')
    kpi_sale_trending_product_value = fields.Many2many('product.product', 'sale_product_digest_rel_ts', 'digest_id', 'product_id', string='Wholesale Trending Products Values',
                                                       compute='_kpi_sale_trending_product_value')

    kpi_salesperson_detail = fields.Boolean('Salesperson Detail')
    kpi_salesperson_detail_value = fields.Many2many('res.users', 'salesperson_user_digest_rel_ts', 'digest_id', 'user_id', string='SalesPerson')

    def _compute_kpis(self, company, user):
        """
        Override because we don't need to calculate margin for many2many fields. So skip it.
        :param company: company
        :param user: user
        :return: dict data
        """
        self.ensure_one()
        digest_fields = self._get_kpi_fields()
        invalid_fields = []
        kpis = [
            dict(kpi_name=field_name,
                 kpi_fullname=self.env['ir.model.fields']._get(self._name, field_name).field_description,
                 kpi_action=False,
                 kpi_col1=dict(),
                 kpi_col2=dict(),
                 kpi_col3=dict(),
                 )
            for field_name in digest_fields
        ]
        kpis_actions = self._compute_kpis_actions(company, user)

        for col_index, (tf_name, tf) in enumerate(self._compute_timeframes(company)):
            digest = self.with_context(start_datetime=tf[0][0], end_datetime=tf[0][1]).with_user(user).with_company(company)
            previous_digest = self.with_context(start_datetime=tf[1][0], end_datetime=tf[1][1]).with_user(user).with_company(company)
            for index, field_name in enumerate(digest_fields):
                kpi_values = kpis[index]
                kpi_values['kpi_action'] = kpis_actions.get(field_name)
                try:
                    compute_value = digest[field_name + '_value']
                    # Context start and end date is different each time so invalidate to recompute.
                    digest.invalidate_cache([field_name + '_value'])
                    previous_value = previous_digest[field_name + '_value']
                    # Context start and end date is different each time so invalidate to recompute.
                    previous_digest.invalidate_cache([field_name + '_value'])
                except AccessError:  # no access rights -> just skip that digest details from that user's digest email
                    invalid_fields.append(field_name)
                    continue
                if self._fields[field_name + '_value'].type == 'many2many':
                    margin = 0.0
                else:
                    margin = self._get_margin_value(compute_value, previous_value)
                if self._fields['%s_value' % field_name].type == 'monetary':
                    converted_amount = tools.format_decimalized_amount(compute_value)
                    compute_value = self._format_currency_amount(converted_amount, company.currency_id)
                kpi_values['kpi_col%s' % (col_index + 1)].update({
                    'value': compute_value,
                    'margin': margin,
                    'col_subtitle': tf_name,
                })

        return [kpi for kpi in kpis if kpi['kpi_name'] not in invalid_fields]

    def get_salesperson_detail_with_duration(self):
        user_details = {}
        data = self._compute_timeframes(self.env.user.company_id)
        data = dict(data)
        for val in ['Last 24 hours', 'Last 7 Days', 'Last 30 Days']:
            dict_val = {}
            for user in self.kpi_salesperson_detail_value:
                dates = data[val]
                from_date, to_date = dates[0][0], dates[0][1]
                quotation_ids = self.env['sale.order'].search(
                    [('date_order', '>=', from_date), ('date_order', '<=', to_date), ('user_id', '=', user.id), ('state', 'in', ('draft', 'sent'))])
                digest_no_of_quotation = len(quotation_ids)

                invoice_ids = self.env['account.move'].sudo().search(
                    [('invoice_date', '>=', from_date), ('invoice_date', '<=', to_date), ('invoice_user_id', '=', user.id), ('move_type', '=', 'out_invoice'),
                     ('state', 'in', ('draft', 'posted'))])
                digest_no_of_invoice = len(invoice_ids)

                total = 0.0
                quotation_ids = self.env['sale.order'].search(
                    [('date_order', '>=', from_date), ('date_order', '<=', to_date), ('user_id', '=', user.id), ('state', 'in', ('draft', 'sent'))])
                for order in quotation_ids:
                    total += order.amount_total
                digest_quotation_total = total

                total = 0.0
                invoice_ids = self.env['account.move'].sudo().search(
                    [('invoice_date', '>=', from_date), ('invoice_date', '<=', to_date), ('invoice_user_id', '=', user.id), ('move_type', '=', 'out_invoice'),
                     ('state', 'in', ('draft', 'posted'))])
                for invoice in invoice_ids:
                    total += invoice.amount_total
                digest_invoice_total = total

                dict_val.update({
                    user.id: {
                        'digest_no_of_quotation': digest_no_of_quotation,
                        'digest_no_of_invoice': digest_no_of_invoice,
                        'digest_quotation_total': digest_quotation_total and round(digest_quotation_total, 2) or 0.0,
                        'digest_invoice_total': digest_invoice_total and round(digest_invoice_total, 2) or 0.0
                    }
                })
                user_details.update({val: dict_val})
        return user_details

    def _kpi_ecommerce_trending_product_value(self):
        for rec in self:
            start, end, company = rec._get_kpi_compute_parameters()
            website_ids = self.env['website'].search([])
            report_details = self.env['sale.report'].read_group(
                domain=[
                    ('website_id', 'in', website_ids.ids),
                    ('state', 'in', ['sale', 'done']),
                    ('date', '>=', start),
                    ('date', '<=', end)
                ],
                fields=['product_id', 'product_uom_qty', 'price_subtotal'],
                groupby='product_id', limit=5)
            product_ids = self.env['product.product']
            for report_detail in report_details:
                product_ids += self.env['product.product'].browse(report_detail['product_id'][0])
            rec.kpi_ecommerce_trending_product_value = product_ids

    def _kpi_pos_trending_product_value(self):
        for rec in self:
            start, end, company = rec._get_kpi_compute_parameters()
            report_details = self.env['report.pos.order'].read_group(
                domain=[
                    ('state', 'in', ['invoiced', 'done', 'paid']),
                    ('date', '>=', start),
                    ('date', '<=', end)
                ],
                fields=['product_id', 'product_qty', 'price_total'],
                groupby='product_id', limit=5)
            product_ids = self.env['product.product']
            for report_detail in report_details:
                product_ids += self.env['product.product'].browse(report_detail['product_id'][0])
            rec.kpi_pos_trending_product_value = product_ids

    def _kpi_sale_trending_product_value(self):
        for rec in self:
            start, end, company = rec._get_kpi_compute_parameters()
            report_details = self.env['sale.report'].read_group(
                domain=[
                    ('website_id', '=', False),
                    ('state', 'in', ['sale', 'done']),
                    ('date', '>=', start),
                    ('date', '<=', end)
                ],
                fields=['product_id', 'product_uom_qty', 'price_subtotal'],
                groupby='product_id', limit=5)
            product_ids = self.env['product.product']
            for report_detail in report_details:
                product_ids += self.env['product.product'].browse(report_detail['product_id'][0])
            rec.kpi_sale_trending_product_value = product_ids

    def _compute_kpi_takealot_capetown_value(self):
        if not self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            confirmed_sales = self.env['sale.order'].search([('date_order', '>=', start),
                                                             ('date_order', '<', end),
                                                             ('partner_id', '=', 3811),
                                                             ('state', 'not in', ['draft', 'cancel', 'sent']),
                                                             ('company_id', '=', company.id)])
            record.kpi_takealot_capetown_value = sum(confirmed_sales.mapped('amount_total'))

    def _compute_kpi_takealot_johannesburg_value(self):
        if not self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            confirmed_sales = self.env['sale.order'].search([('date_order', '>=', start),
                                                             ('date_order', '<', end),
                                                             ('partner_id', '=', 3812),
                                                             ('state', 'not in', ['draft', 'cancel', 'sent']),
                                                             ('company_id', '=', company.id)])
            record.kpi_takealot_johannesburg_value = sum(confirmed_sales.mapped('amount_total'))

    def _compute_kpi_takealot_capetown_count_value(self):
        if not self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            confirmed_sales = self.env['sale.order'].search_count([('date_order', '>=', start),
                                                                   ('date_order', '<', end),
                                                                   ('partner_id', '=', 3811),
                                                                   ('state', 'not in', ['draft', 'cancel', 'sent']),
                                                                   ('company_id', '=', company.id)])
            record.kpi_takealot_capetown_count_value = confirmed_sales

    def _compute_kpi_takealot_johannesburg_count_value(self):
        if not self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            confirmed_sales = self.env['sale.order'].search_count([('date_order', '>=', start),
                                                                   ('date_order', '<', end),
                                                                   ('partner_id', '=', 3812),
                                                                   ('state', 'not in', ['draft', 'cancel', 'sent']),
                                                                   ('company_id', '=', company.id)])
            record.kpi_takealot_johannesburg_count_value = confirmed_sales
