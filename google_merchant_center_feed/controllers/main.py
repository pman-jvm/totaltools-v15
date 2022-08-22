# -*- encoding: utf-8 -*-

from odoo import http
from odoo.tools import misc
from odoo.http import request
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.addons.website_google_merchant_center.models.google_merchant_center import get_unique_id


class GoogleMerchantCenterFeeds(http.Controller):

    @http.route('/gmc/feeds/<int:company>/', type='http', auth="none")
    def gmc_feeds(self, company, **kw):
        """ This route/function is called by Google when user Accept/Refuse the consent of Google """
        web_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')

        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        # template_vals = {'title': '', 'link': web_base_url, 'description': ''}
        # items = []
        xml = """<?xml version="1.0"?>
<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">
<channel>
<link>{link}</link>""".format(link=web_base_url)
        xml_product_line = ""
        for product in request.env['product.product'].sudo().with_env(request.env(user=SUPERUSER_ID, su=True)).search(
                [('sync_with_mc', '=', True), ('website_published', '=', True), ('google_product_brand_id', '!=', False), ('google_merchant_center_id', '!=', False)]):
            if product.google_mcid:
                offerId = product.google_mcid
                product.write({'google_sync_date': fields.Date.today()})
            else:
                offerId = 'CM%s' % get_unique_id()
                product.write({'google_mcid': offerId, 'google_sync_date': fields.Date.today()})
            # Display ads id
            if product.google_display_ads_id:
                displayAdsId = product.google_display_ads_id
            else:
                displayAdsId = 'ADS%s' % get_unique_id()
                product.write({'google_display_ads_id': displayAdsId})

            link = product.google_merchant_center_id.website + "/shop/product/%s" % (product.product_tmpl_id.id,)
            imageLink = product.google_merchant_center_id.website + '/web/image/%s/%s/%s/image.jpg' % ('product.template', product.product_tmpl_id.id, 'image_1024')
            price_with_currency = "{} {}".format(round(product.gmc_list_price, 2), product.currency_id.name)
            shipping_price_with_currency = "{} {}".format(product.google_shipping_amount, product.currency_id.name)
            brand = product.google_product_brand_id and product.google_product_brand_id.name or ''
            product_type = " > ".join(reversed(get_names(product.categ_id)))
            google_product_category = " > ".join(reversed(get_names(product.google_product_category_id)))
            xml_product_line += "<item>"
            if offerId:
                xml_product_line += "<g:id>{}</g:id>".format(offerId)
            if product.name:
                xml_product_line += "<g:title>{}</g:title>".format(misc.html_escape(product.name))
            if product.description_sale:
                xml_product_line += "<g:description>{}</g:description>".format(misc.html_escape(product.description_sale))
            if link:
                xml_product_line += "<g:link>{}</g:link>".format(link)
            if imageLink:
                xml_product_line += "<g:image_link>{}</g:image_link>".format(imageLink)
            if product.google_condition:
                xml_product_line += "<g:condition>{}</g:condition>".format(product.google_condition)
            if product.google_availability:
                xml_product_line += "<g:availability>{}</g:availability>".format(product.google_availability)
            if price_with_currency:
                xml_product_line += "<g:price>{}</g:price>".format(price_with_currency)

            xml_product_line += "<g:shipping>"
            if product.google_target_country:
                xml_product_line += "<g:country>{}</g:country>".format(product.google_target_country)
            if product.google_shipping:
                xml_product_line += "<g:service>{}</g:service>".format(product.google_shipping)
            if shipping_price_with_currency:
                xml_product_line += "<g:price>{}</g:price>".format(shipping_price_with_currency)
            xml_product_line += "</g:shipping>"

            if not product.google_barcode_as_gtin and product.google_gtin:
                xml_product_line += "<g:gtin>{}</g:gtin>".format(product.google_gtin)
            elif product.google_barcode_as_gtin and product.barcode:
                xml_product_line += "<g:gtin>{}</g:gtin>".format(product.barcode)
            if brand:
                xml_product_line += "<g:brand>{}</g:brand>".format(brand)
            if product.google_identifier_exists:
                xml_product_line += "<g:mpn>{}</g:mpn>".format(product.default_code)
            if product_type:
                xml_product_line += "<g:product_type>{}</g:product_type>".format(misc.html_escape(product_type))
            if google_product_category:
                xml_product_line += "<g:google_product_category>{}</g:google_product_category>".format(misc.html_escape(google_product_category))
            xml_product_line += "</item>"
            # product_data = {
            #     'offerId': offerId,
            #     'displayAdsId': displayAdsId,
            #     'title': product.name,
            #     'description': product.description_sale,
            #     # Use product template url as variants are not shown sepratly.
            #     'link': product.google_merchant_center_id.website + "/shop/product/%s" % (product.product_tmpl_id.id,),
            #     'imageLink': product.google_merchant_center_id.website + '/web/image/%s/%s/%s/image.jpg' % ('product.template', product.product_tmpl_id.id, 'image_1024'),
            #     # Note: Instead of passing website url passsed backend URl because Store not accept image without type
            #     'contentLanguage': product.google_content_language,
            #     'targetCountry': product.google_target_country,
            #     'channel': product.google_channel,
            #     'availability': product.google_availability,
            #     'condition': product.google_condition,
            #     'googleProductCategory': " > ".join(reversed(get_names(product.google_product_category_id))),
            #     'productType': " > ".join(reversed(get_names(product.categ_id))),
            #     'brand': product.google_product_brand_id and product.google_product_brand_id.name or '',
            #     'price_with_currency': "{} {}".format(round(product.gmc_list_price, 2), product.currency_id.name),
            #     'shipping': {
            #         'country': product.google_target_country,
            #         'service': product.google_shipping,
            #         'price_with_currency': "{} {}".format(product.google_shipping_amount, product.currency_id.name)
            #     },
            # }

            # Check if identifierExists than only add mpn
            # if product.google_identifier_exists:
            #     product_data.update({'mpn': product.default_code})
            # if not product.google_barcode_as_gtin and product.google_gtin:
            #     product_data.update({'gtin': product.google_gtin})
            # elif product.google_barcode_as_gtin and product.barcode:
            #     product_data.update({'gtin': product.barcode})
            # else:
            #     product_data.update({'identifierExists': 'no'})
            # items.append(product_data)
            # template_vals.update({'items': items})

            # xml += request.env['ir.qweb'].render('google_merchant_center_feed.gmc_feed_template', template_vals)
        xml += xml_product_line
        xml += """</channel>
</rss>"""
        xmlheaders = [('Content-Type', 'application/xml'), ('Content-Disposition', 'attachment; filename=gmc_feed.xml;')]
        return request.make_response(xml, headers=xmlheaders)
