import io
import base64
from PyPDF2 import PdfFileReader, PdfFileWriter
from odoo.http import request, route, Controller


class CatalogPricelistReportTS(Controller):

    @route(["/print/catalog_pricelist_report_ts"], type='http', auth='user')
    def get_catalog_pricelist_report_ts(self, report_data={}, wizard_id=False, **post):
        if not wizard_id:
            return False
        form_data = request.env['catalog.pricelist.report.wizard'].browse(int(wizard_id)).read()[0]
        if not report_data or not form_data:
            return False
        categ_obj = request.env['product.category']
        pdf_writer = PdfFileWriter()
        for categ_id, product_ids in eval(report_data).items():
            categ = categ_obj.browse(categ_id)
            datas = {
                'ids': product_ids,
                'model': 'product.product',
                # 'form': eval(form_data),
                'form': form_data,
            }
            cover_page = categ.cover_page_pdf and base64.b64decode(categ.cover_page_pdf) or b''
            cover_reader = cover_page and PdfFileReader(io.BytesIO(cover_page), strict=False, overwriteWarnings=False) or []
            if cover_reader:
                for page in range(cover_reader.getNumPages()):
                    pdf_writer.addPage(cover_reader.getPage(page))
            pdf_data = request.env.ref('catalog_pricelist_report.action_catalog_report')._render_qweb_pdf([], data=datas)[0]
            reader = PdfFileReader(io.BytesIO(pdf_data), strict=False, overwriteWarnings=False)
            for page in range(reader.getNumPages()):
                pdf_writer.addPage(reader.getPage(page))
        _buffer = io.BytesIO()
        pdf_writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()
        report_name = "Catalog PriceList Report"
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(merged_pdf)),
            ('Content-Disposition', 'attachment; filename=' + report_name + '.pdf;')
        ]
        return request.make_response(merged_pdf, headers=pdfhttpheaders)
