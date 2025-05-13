from odoo import http
from odoo.http import request
import json

class PropertyAPI(http.Controller):

    @http.route("/v1/api/property", methods=["POST"], auth="none", type="http", csrf=False)
    def post_property_endpoint(self):
        args = request.httprequest.data.decode('utf-8')
        vals = json.loads(args)
        print(vals)
        if not vals.get('name'):
            return request.make_json_response({
                "error": "name is required"
            }, status=400)
        try:
            res = request.env['property'].sudo().create(vals)
            print(res)
            return request.make_json_response({
                "message": "property has been created",
                "id": res.id,
                "name": res.name
            }, status=201)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/property/json", methods=["POST"], auth="none", type="json", csrf=False)
    def post_property_json(self):

        try:
            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)
            res = request.env['property'].sudo().create(vals)
            return {
                "message": "property has been created",
                "id": res.id,
                "name": res.name
            }
        except Exception as e:
            return {
                "error": str(e)
            }


    @http.route("/v1/api/property/<int:property_id>", methods=["PUT"], auth="none", type="http", csrf=False)
    def update_property(self, property_id):

        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "id is not exist"
                }, status=400)

            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)
            print(vals)
            property_id.write(vals)
            print(property_id.garden_area)
            return request.make_json_response({
                "message": "property has been updated",
                "id": property_id.id,
                "name": property_id.name
            }, status=201)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

