import math
from odoo.http import request
from odoo import http
from urllib.parse import parse_qs
import json


def valid_response(data , status):
    response_body = {
        'data' : data,
        'message' : "successful"
    }
    return request.make_json_response(response_body, status=status)

def invalid_response(error , status):
    response_body = {
        'error' : error
    }
    return request.make_json_response(response_body, status=status)


class PropertyAPI(http.Controller):

    # @http.route("/v1/api/property", methods=["POST"], auth="none", type="http", csrf=False)
    # def post_property_endpoint(self):
    #     try:
    #         args = request.httprequest.data.decode('utf-8')
    #         vals = json.loads(args)
    #         if not vals.get('name'):
    #             return invalid_response({
    #                 "error": "name is required"
    #             }, status=400)
    #         res = request.env['property'].sudo().create(vals)
    #         return valid_response({
    #             "message": "property has been created",
    #             "id": res.id,
    #             "name": res.name
    #         }, status=201)
    #     except Exception as e:
    #         return invalid_response({
    #             "error": str(e)
    #         }, status=400)

    @http.route("/v1/api/property", methods=["POST"], auth="none", type="http", csrf=False)
    def post_property_endpoint(self):
        try:
            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)
            if not vals.get('name'):
                return invalid_response({
                    "error": "name is required"
                }, status=400)
            if isinstance(vals.get("name"), (dict, list, str)):
                vals["name"] = json.dumps(vals["name"])
            cr = request.env.cr
            columns = ", ".join(vals.keys())
            values = ", ".join(["%s"] * len(vals))
            query = f"""
                           INSERT INTO property ({columns})
                           VALUES ({values}) 
                           RETURNING id, name, postcode
                       """
            cr.execute(query, tuple(vals.values()))
            res = cr.fetchone()
            print(res)
            return valid_response({
                "message": "property has been created",
                "id": res[0],
                "name": res[1],
                "postcode":res[2]
            }, status=201)
        except Exception as e:
            return invalid_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/property/json", methods=["POST"], auth="none", type="json", csrf=False)
    def post_property_json(self):

        try:
            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)
            res = request.env['property'].sudo().create(vals)
            return valid_response({
                "message": "property has been created",
                "id": res.id,
                "name": res.name
            }, status= 200)
        except Exception as e:
            return invalid_response({
                "error": str(e)
            }, status = 400)


    @http.route("/v1/api/property/<int:property_id>", methods=["PUT"], auth="none", type="http", csrf=False)
    def update_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response({
                    "error": "id is not exist"
                }, status=400)
            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)
            print(vals)
            property_id.write(vals)
            print(property_id.garden_area)
            return valid_response({
                "message": "property has been updated",
                "id": property_id.id,
                "name": property_id.name
            }, status=200)
        except Exception as e:
            return invalid_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/property/<int:property_id>", methods=["GET"], auth="none", type="http", csrf=False)
    def read_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response({
                    "error": "id is not exist"
                }, status=400)
            return valid_response({
                "id": property_id.id,
                "name": property_id.name,
                "ref": property_id.ref,
                "postcode":property_id.postcode,
                "date_availability": property_id.date_availability,
                "expected_date": property_id.expected_date,
                "bedrooms":property_id.bedrooms,
                "owner_id": property_id.owner_id,
            }, status=200)
        except Exception as e:
            return invalid_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/property/<int:property_id>", methods=["DELETE"], auth="none", type="http", csrf=False)
    def delete_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response({
                    "error": "id is not exist"
                }, status=400)
            property_id.unlink()
            return valid_response({
                "message": "property has been deleted"
            }, status=201)
        except Exception as e:
            return invalid_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/properties", methods=["GET"], auth="none", type="http", csrf=False)
    def read_all_properties(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            page = offset = None
            limit = 5
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])
                if page:
                    offset = (page * limit) - limit
            if params.get('state'):
                property_domain += [('state', '=', params.get('state')[0])]
            property_ids = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit, order='id DESC')
            property_count= request.env['property'].sudo().search_count(property_domain)


            if not property_ids:
                return invalid_response({
                    "error": "there are not records"
                }, status=400)
            return valid_response({
                "total": property_count,
                "pages": math.ceil(property_count / limit) if limit else 1 ,
                "page": page or 1,
                "limit": limit,
                "results": [{
                    "id": property_id.id,
                    "name": property_id.name,
                    "ref": property_id.ref,
                    "postcode": property_id.postcode,
                    "date_availability": property_id.date_availability,
                    "expected_date": property_id.expected_date,
                    "bedrooms": property_id.bedrooms,
                    "owner_id": {
                        "id": property_id.owner_id.id,
                        "name": property_id.owner_id.name
                    }
                } for property_id in property_ids]
            }, status=200)
        except Exception as e:
            return invalid_response({
                "error": str(e)
            }, status=400)
