from odoo import models, fields
import logging
from xlrd import open_workbook
from xlrd.timemachine import xrange

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    image_url = fields.Char("Image URL", copy=False, compute='_compute_image_url')
    create_from_sheet = fields.Boolean(string="Create From Sheet", default=False, copy=False)
    country_origin_id = fields.Many2one('res.country', string='Country of Origin', default=lambda self: self.env.company.country_id, copy=False)
    catalogue_page = fields.Integer("Catalogue Page", copy=False)
    depth = fields.Float("Depth")

    def _compute_image_url(self):
        for product in self:
            product.image_url = 'https://www.altiven.co.za/web/image?model=product.template&id={}&field=image_1024'.format(product.id)

    def test(self):
        import base64
        import urllib
        import logging
        from xlrd import open_workbook
        from xlrd.timemachine import xrange
        _logger = logging.getLogger(__name__)
        book = open_workbook('/home/teju/Desktop/t/Altiven/SEALEY WEBSITE LINKS (VLOOKUP) (3).xlsx')
        book2 = open_workbook('/home/teju/Desktop/t/Altiven/Datacut_4_Export_Models_Images_videos.xlsx')
        sheet = book.sheet_by_index(0)
        sheet2 = book2.sheet_by_index(0)
        # read header values into the list
        keys = [sheet.cell(1, col_index).value for col_index in xrange(sheet.ncols)]
        keys2 = [sheet2.cell(0, col_index).value for col_index in xrange(sheet2.ncols)]
        dict_list = []
        image_dict_list = []
        start_range = 2
        end_range = 102
        # for row_index in xrange(start_range, sheet.nrows):
        for row_index in xrange(start_range, end_range):
            d = {keys[col_index]: sheet.cell(row_index, col_index).value for col_index in xrange(sheet.ncols)}
            dict_list.append(d)

        for row_index in xrange(start_range, end_range):
            d = {keys2[col_index]: sheet2.cell(row_index, col_index).value for col_index in xrange(sheet2.ncols)}
            image_dict_list.append(d)

        categ_obj = self.env['product.category']
        product_tmpl_obj = self.env['product.template']
        public_categ_obj = self.env['product.public.category']
        country_obj = self.env['res.country']
        existing_products = []
        ctr = 0
        for row in dict_list:
            ctr += 1
            try:
                product = product_tmpl_obj.search([('default_code', '=', row['Model Number'])])
                if product:
                    existing_products.append(product.default_code)
                    continue
                else:
                    categ_id = categ_obj.search([('name', '=', row['Category'])])
                    if not categ_id:
                        categ_id = categ_obj.create({'name': row['Category']})
                    if row['Group']:
                        child_cat = categ_obj.search([('name', '=', row['Group'])])
                        if not child_cat:
                            categ_id = categ_obj.create({'name': row['Group'], 'parent_id': categ_id.id})
                        else:
                            categ_id = child_cat
                    if row['Microgroup']:
                        micro_cat = categ_obj.search([('name', '=', row['Microgroup'])])
                        if not micro_cat:
                            categ_id = categ_obj.create({'name': row['Microgroup'], 'parent_id': categ_id.id})
                        else:
                            categ_id = micro_cat
                    public_categ_id = public_categ_obj.search([('name', '=', row['Category'])])
                    if not public_categ_id:
                        public_categ_id = public_categ_obj.create({'name': row['Category']})
                    if row['Group']:
                        child_cat = public_categ_obj.search([('name', '=', row['Group'])])
                        if not child_cat:
                            public_categ_id = public_categ_obj.create({'name': row['Group'], 'parent_id': public_categ_id.id})
                        else:
                            public_categ_id = child_cat
                    if row['Microgroup']:
                        micro_cat = public_categ_obj.search([('name', '=', row['Microgroup'])])
                        if not micro_cat:
                            public_categ_id = public_categ_obj.create({'name': row['Microgroup'], 'parent_id': public_categ_id.id})
                        else:
                            public_categ_id = micro_cat
                    country_origin_id = country_obj.search([('code_alpha3', '=', row['COO'])])
                    country_origin_id = country_origin_id.id if country_origin_id else False
                    image_list = [item for item in image_dict_list if item['ModelNo3'] == row['Model Number']]
                    main_image = [item for item in image_list if item['FileType'] == 'Web Main Picture']
                    extra_image_list = [item for item in image_list if item['FileType'] == 'Web Image']
                    main_image_path, main_image_name = '', ''
                    if main_image:
                        main_image_path = main_image[0]['ArchivePath'].replace('\\\\', '/').replace('\\', '/')
                        main_image_name = main_image[0]['FileName']
                    if extra_image_list:
                        extra_image_url_list = []
                        for extra_image in extra_image_list:
                            extra_image_name = extra_image['FileName']
                            extra_image_url_list.append(extra_image_name)
                    if main_image:
                        urllib.request.urlretrieve('ftp://sealey-spip:vYnnS3*m@sealey.iweb-storage.com/Protected/MasterData/Images/WEBMain/{}'.format(main_image_name),
                                                   '/tmp/ftp/{}'.format(main_image_name))
                    if extra_image_list:
                        for extra_image in extra_image_url_list:
                            urllib.request.urlretrieve('ftp://sealey-spip:vYnnS3*m@sealey.iweb-storage.com/Protected/MasterData/Images/WEBImage/{}'.format(extra_image),
                                                       '/tmp/ftp/{}'.format(extra_image))
                    product_dict = {'name': row['Description'],
                                    'type': 'product',
                                    'default_code': row['Model Number'],
                                    'uom_id': 1,
                                    # 'uom_po_id': 1,
                                    # 'marketplace_seller_id': 7,
                                    'categ_id': categ_id and categ_id.id or 1,
                                    'public_categ_ids': [(4, public_categ_id.id)] if public_categ_id else [],
                                    # 'price_code': row['Price Code'] or '',
                                    # 'catalogue_page': row['CATALOGUE PAGE'] and int(row['CATALOGUE PAGE']) or None,
                                    'hs_code': row['COMMODITY CODE'],
                                    # 'net_weight': row['Net Wt (Kg)'],
                                    'barcode': row['EAN'],
                                    'list_price': row['Salling price'] and float(row['Salling price'].replace(",", "")) or 0.0,
                                    'standard_price': row['Purchase price'] and float(row['Purchase price'].replace(",", "")) or 0.0,
                                    # 'currency_id': 147,
                                    'country_origin_id': country_origin_id,
                                    'height': row['Height'],
                                    'width': row['Width'],
                                    'depth': row['Depth'],
                                    'volume': row['Total Volume'],
                                    'weight': row['Gross Weight'],
                                    # 'status': 'approved',
                                    'sale_ok': True,
                                    'sync_with_mc': False,
                                    # 'website_description': row['PT'],
                                    # 'description_sale': row['Web Text'],
                                    # 'analysis_code': row['Analysis Code'],
                                    'create_from_sheet': True,
                                    }
                    if main_image_name:
                        image_path = '/tmp/ftp/{}'.format(main_image_name)
                        with open(image_path, "rb") as img_obj:
                            encoded_string = base64.b64encode(img_obj.read())
                            img_obj.close()
                            product_dict.update({'image_1920': encoded_string})
                    if extra_image_url_list:
                        product_template_image_ids = []
                        for extra_image_url in extra_image_url_list:
                            image_path = '/tmp/ftp/{}'.format(extra_image_url)
                            with open(image_path, "rb") as img_obj:
                                encoded_string = base64.b64encode(img_obj.read())
                                img_obj.close()
                                product_template_image_ids.append((0, 0, {'image_1920': encoded_string, 'name': row['Description']}))
                        product_dict.update({'product_template_image_ids': product_template_image_ids})
                    product_id = product_tmpl_obj.create(product_dict)
                    _logger.info([{'Total create product': ctr, 'SKU': product_id.default_code}])
                    if ctr % 100 == 0:
                        self._cr.commit()
            except Exception as e:
                _logger.error("Error while processing {} product. ERROR: {}".format(row['Model Number'], e))
        result = "Start From: {}, Stop to: {} and Existing products: {}".format(start_range, end_range, existing_products)


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def binary_content(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                       unique=False, filename=None, filename_field='name', download=False,
                       mimetype=None, default_mimetype='application/octet-stream',
                       access_token=None):
        obj = None
        if xmlid:
            obj = self._xmlid_to_obj(self.env, xmlid)
        elif id and model in self.env:
            obj = self.env[model].browse(int(id))
        if obj and 'website_published' in obj._fields:
            self = self.sudo()
            # if self.env[obj._name].sudo().search([('id', '=', obj.id), ('website_published', '=', True)]):
            #     self = self.sudo()
        return super(Http, self).binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype,
            default_mimetype=default_mimetype, access_token=access_token)
