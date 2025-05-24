from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval

class XlsxOwnerReport(http.Controller):

    @http.route("/owner/excel/report/<string:owner_ids>", auth="user", type="http")
    def download_owner_excel_report(self, owner_ids):
        try:
            owner_ids = request.env['owner'].browse(literal_eval(owner_ids))

            # 1. Create
            output = io.BytesIO()

            # 2. Create an Excel workbook in memory
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet('owners')

            #  3. Formats
            header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
            string_format = workbook.add_format({'border': 1, 'align': 'center'})


            # 4. Write headers in the first row
            headers = [
                'Owner Name', 'Owner Address', 'Owner Phone','Owner mail','Properties'
            ]
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, header_format)

            # 5. write data
            row_num = 1
            for owner in owner_ids:
                worksheet.write(row_num, 0, owner.name or '', string_format)
                worksheet.write(row_num, 1, owner.address or '', string_format)
                worksheet.write(row_num, 2, owner.phone_number or '', string_format)
                worksheet.write(row_num, 3, owner.e_mail or '', string_format)
                property_names = ', '.join(owner.property_ids.mapped('name'))
                worksheet.write(row_num, 4, property_names, string_format)
                row_num += 1


            # 6. Close workbook and reset pointer
            workbook.close()
            output.seek(0)

            # 7. owner file name and return response
            file_name = 'owner_Report.xlsx'
            return request.make_response(
                output.getvalue(),
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', f'attachment; filename="{file_name}"')
                ]
            )
        except Exception as e:
            return request.make_response(f"Error generating report: {str(e)}", status=500)


