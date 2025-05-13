from odoo import http

class TestAPI(http.Controller):
    @http.route('/api/test',methods=["GET"], auth='none', type='http', csrf=False)
    def test_endpoint(self):
        return "Hello, World! '.;',l;mkjbvnhjmk,n"
