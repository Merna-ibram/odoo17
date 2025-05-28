from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval

class XlsxToDoReport(http.Controller):

    @http.route("/todo/excel/report/<string:task_ids>", auth="user", type="http")
    def download_todo_excel_report(self, task_ids):
        try:
            task_ids = request.env['todo.list'].browse(literal_eval(task_ids))

            # 1. Create
            output = io.BytesIO()

            # 2. Create an Excel workbook in memory
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet('tasks')

            #  3. Formats
            header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
            string_format = workbook.add_format({'border': 1, 'align': 'center'})



            # 4. Write headers in the first row
            headers = [
                'id', 'ref', 'name','assign_to','expected_date','due_date', 'state', 'description'
            ]
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, header_format)

            # 5. write data
            row_num = 1
            for task in task_ids:
                worksheet.write(row_num, 0, task.id or '', string_format)
                worksheet.write(row_num, 1, task.ref or '', string_format)
                worksheet.write(row_num, 2, task.name or '', string_format)
                worksheet.write(row_num, 3, task.assign_to.name  or '', string_format)
                worksheet.write(row_num, 4, str(task.expected_date or ''), string_format)
                worksheet.write(row_num, 5, str(task.due_date or ''), string_format)
                worksheet.write(row_num, 6, dict(task._fields['state'].selection).get(task.state, ''),string_format)
                worksheet.write(row_num, 7, task.description or '', string_format)
                row_num += 1

            # 6. Close workbook and reset pointer
            workbook.close()
            output.seek(0)

            # 7. Prepare file name and return response
            file_name = 'Tasks_Report.xlsx'
            return request.make_response(
                output.getvalue(),
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', f'attachment; filename="{file_name}"')
                ]
            )
        except Exception as e:
            return request.make_response(f"Error generating report: {str(e)}", status=500)


