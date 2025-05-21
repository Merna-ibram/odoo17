from urllib.parse import parse_qs
from odoo import http
from odoo.http import request
import json
import math

class TOdoAPI(http.Controller):

    @http.route("/v1/api/todo.list", methods=["POST"], auth="none", type="http", csrf=False)
    def create_task(self):
        try:
            args = request.httprequest.data.decode('utf-8')
            data = json.loads(args)
            vals = data.get('task', data)
            if not vals.get('name'):
                return request.make_json_response({
                    "error": "name is required"
                }, status=400)

            if isinstance(vals.get('assign_to'), dict):
                vals['assign_to'] = vals['assign_to'].get('id')

            lines = vals.pop('task_line_ids', [])
            vals['task_line_ids'] = [(0, 0, line) for line in lines]
            vals.pop('is_late', None)
            res = request.env['todo.list'].sudo().create(vals)
            return request.make_json_response({
                "message": "Task has been created successfully.",
                "id": res.id,
                "name": res.name,
                "state": res.state,
                "description": res.description,
                "due_date": str(res.due_date),
                "expected_date": str(res.expected_date),
                "assign_to": res.assign_to.name if res.assign_to else None
            }, status=201)

        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/todo.list/<int:todo_list_id>", methods=["DELETE"], auth="none", type="http", csrf=False)
    def delete_task(self, todo_list_id):
        try:
            todo_list_id = request.env['todo.list'].sudo().search([('id', '=', todo_list_id)])
            if not todo_list_id:
                return request.make_json_response({
                    "message": "id is not exist"
                }, status=400)
            todo_list_id.unlink()
            return request.make_json_response({
                "message": "task has been deleted"
            }, status=201)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/todo.list/<int:todo_list_id>", methods=["PUT"], auth="none", type="http", csrf=False)
    def update_task(self, todo_list_id):
        try:
            todo_list_id = request.env['todo.list'].sudo().search([('id', '=', todo_list_id)])
            if not todo_list_id:
                return request.make_json_response({
                    "message": "id is not exist"
                }, status=400)
            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)
            print(vals)
            todo_list_id.write(vals)
            print(todo_list_id.state)
            return request.make_json_response({
                "message": "task has been updated",
                 "id": todo_list_id.id,
                "name": todo_list_id.name,
                "state": todo_list_id.state,
                "description": todo_list_id.description,
                "due_date": str(todo_list_id.due_date),
                "expected_date": str(todo_list_id.expected_date),
                "assign_to": todo_list_id.assign_to.name if todo_list_id.assign_to else None
            }, status=200)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

    @http.route("/v1/api/todo.list/<int:todo_list_id>", methods=["GET"], auth="none", type="http", csrf=False)
    def read_owner(self, todo_list_id):
        try:
            todo_list_id = request.env['todo.list'].sudo().search([('id', '=', todo_list_id)])
            if not todo_list_id:
                return request.make_json_response({
                    "message": "id is not exist"
                }, status=400)
            return request.make_json_response({
                 "id": todo_list_id.id,
                 "name": todo_list_id.name,
                 "state": todo_list_id.state,
                 "description": todo_list_id.description,
                 "due_date": str(todo_list_id.due_date),
                 "expected_date": str(todo_list_id.expected_date),
                 "assign_to": todo_list_id.assign_to.name if todo_list_id.assign_to else None
            }, status=200)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)



    @http.route("/v1/api/todo.list", methods=["GET"], auth="none", type="http", csrf=False)
    def read_all_tasks(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            task_domain = []
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
                task_domain += [('name', '=', params.get('name')[0])]
            todo_list_ids = request.env['todo.list'].sudo().search(task_domain,  offset=offset, limit=limit, order='id DESC')
            todo_list_count= request.env['todo.list'].sudo().search_count(task_domain)

            if not todo_list_ids:
                return request.make_json_response({
                    "message": "there are not records"
                }, status=400)
            return request.make_json_response({
                "total": todo_list_count,
                "pages": math.ceil(todo_list_count / limit) if limit else 1,
                "page": page or 1,
                "limit": limit,
                "results": [{
                    "id": todo_list_id.id,
                    "name": todo_list_id.name,
                    "state": todo_list_id.state,
                    "description": todo_list_id.description,
                    "due_date": str(todo_list_id.due_date),
                    "expected_date": str(todo_list_id.expected_date),
                    "assign_to": todo_list_id.assign_to.name if todo_list_id.assign_to else None
            } for todo_list_id in todo_list_ids]
            }, status=200)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)
