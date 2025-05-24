from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval

class XlsxPropertyReport(http.Controller):

    @http.route("/property/excel/report/<string:property_ids>", auth="user", type="http")
    def download_property_excel_report(self, property_ids):
        try:
            property_ids = request.env['property'].browse(literal_eval(property_ids))

            # 1. Create
            output = io.BytesIO()

            # 2. Create an Excel workbook in memory
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet('properties')

            #  3. Formats
            header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
            string_format = workbook.add_format({'border': 1, 'align': 'center'})
            price_format = workbook.add_format({'border': 1, 'align': 'center', 'num_format': '$##,###00.000'})



            # 4. Write headers in the first row
            headers = [
                'Ref', 'Name', 'Postcode', 'Description',
                'Available From', 'Expected Date',
                'Expected Price', 'Selling Price', 'Bedrooms',
                'Living Area', 'Facades', 'Garage', 'Garden',
                'Garden Area', 'Garden Orientation',
                'Owner Name', 'Owner Address', 'Owner Phone',
                'State'
            ]
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, header_format)

            # 5. write data
            row_num = 1
            for property in property_ids:
                worksheet.write(row_num, 0, property.ref or '', string_format)
                worksheet.write(row_num, 1, property.name or '', string_format)
                worksheet.write(row_num, 2, property.postcode or '', string_format)
                worksheet.write(row_num, 3, property.description or '', string_format)
                worksheet.write(row_num, 4, str(property.date_availability or ''), string_format)
                worksheet.write(row_num, 5, str(property.expected_date or ''), string_format)
                worksheet.write(row_num, 6, property.expected_price or 0.0, price_format)
                worksheet.write(row_num, 7, property.selling_price or 0.0, price_format)
                worksheet.write(row_num, 8, property.bedrooms or 0, string_format)
                worksheet.write(row_num, 9, property.living_area or 0, string_format)
                worksheet.write(row_num, 10, property.facades or 0, string_format)
                worksheet.write(row_num, 11, 'Yes' if property.garage else 'No', string_format)
                worksheet.write(row_num, 12, 'Yes' if property.garden else 'No', string_format)
                worksheet.write(row_num, 13, property.garden_area or 0, string_format)
                worksheet.write(row_num, 14, property.garden_orientation or '', string_format)
                worksheet.write(row_num, 15, property.owner_id.name if property.owner_id else '', string_format)
                worksheet.write(row_num, 16, property.owner_address or '', string_format)
                worksheet.write(row_num, 17, property.owner_phone_number or '', string_format)
                worksheet.write(row_num, 18, dict(property._fields['state'].selection).get(property.state, ''),string_format)
                row_num += 1

            # 6. Close workbook and reset pointer
            workbook.close()
            output.seek(0)

            # 7. Prepare file name and return response
            file_name = 'Property_Report.xlsx'
            return request.make_response(
                output.getvalue(),
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', f'attachment; filename="{file_name}"')
                ]
            )
        except Exception as e:
            return request.make_response(f"Error generating report: {str(e)}", status=500)


