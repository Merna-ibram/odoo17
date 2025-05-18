from urllib.parse import parse_qs
from odoo import http
from odoo.http import request
import json

class OwnerAPI(http.Controller):

    @http.route("/v1/api/owner", methods=["POST"], auth="none", type="http", csrf=False)
    def post_owner(self):
        try:
            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)
            print(vals)
            if not vals.get('name'):
                return request.make_json_response({
                    "error": "name is required"
                }, status=400)
            res = request.env['owner'].sudo().create(vals)
            print(res)
            return request.make_json_response({
                "message": "owner has been created",
                "id": res.id,
                "name": res.name,
                "phone_number" : res.phone_number,
                "address": res.address,
                "e_mail": res.e_mail
            }, status=201)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)


    @http.route("/v1/api/owner/<int:owner_id>", methods=["PUT"], auth="none", type="http", csrf=False)
    def update_owner(self, owner_id):
        try:
            owner_id = request.env['owner'].sudo().search([('id', '=', owner_id)])
            if not owner_id:
                return request.make_json_response({
                    "message": "id is not exist"
                }, status=400)
            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)
            print(vals)
            owner_id.write(vals)
            print(owner_id.address)
            return request.make_json_response({
                "message": "owner has been updated",
                "id": owner_id.id,
                "name": owner_id.name,
                "phone_number": owner_id.phone_number,
                "address" : owner_id.address,
                "e_mail": owner_id.e_mail
            }, status=200)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/owner/<int:owner_id>", methods=["GET"], auth="none", type="http", csrf=False)
    def read_owner(self, owner_id):
        try:
            owner_id = request.env['owner'].sudo().search([('id', '=', owner_id)])
            if not owner_id:
                return request.make_json_response({
                    "message": "id is not exist"
                }, status=400)
            return request.make_json_response({
                "id": owner_id.id,
                "name": owner_id.name,
                "phone_number": owner_id.phone_number,
                "address" : owner_id.address,
                "e_mail": owner_id.e_mail
            }, status=200)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/owner/<int:owner_id>", methods=["DELETE"], auth="none", type="http", csrf=False)
    def delete_owner(self, owner_id):
        try:
            owner_id = request.env['owner'].sudo().search([('id', '=', owner_id)])
            if not owner_id:
                return request.make_json_response({
                    "message": "id is not exist"
                }, status=400)
            owner_id.unlink()
            return request.make_json_response({
                "message": "owner has been deleted"
            }, status=201)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/owners", methods=["GET"], auth="none", type="http", csrf=False)
    def read_all_owners(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            owner_domain = []
            page = offset = None
            limit = 5
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])
            if page:
                offset = (page * limit) - limit
            if params.get('name'):
                owner_domain += [('name', '=', params.get('name')[0])]
            owner_ids = request.env['owner'].sudo().search(owner_domain,  offset=offset, limit=limit, order='id DESC')
            if not owner_ids:
                return request.make_json_response({
                    "message": "there are not records"
                }, status=400)
            return request.make_json_response([{
                 "id": owner_id.id,
                "name": owner_id.name,
                "phone_number": owner_id.phone_number,
                "address" : owner_id.address,
                "e_mail": owner_id.e_mail
            } for owner_id in owner_ids], status=200)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)
