#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

from app import app

api = Api(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'diego':
        return 'python'
    return None

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

members = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False,
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False,
    }
]

member_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('member')
}

class MemberListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No member title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(MemberListAPI, self).__init__()

    def get(self):
        return {'members': [marshal(member, member_fields) for member in members]}

    def post(self):
        args = self.reqparse.parse_args()
        member = {
            'id': members[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        members.append(member)
        return {'member': marshal(member, member_fields)}, 201


class MemberAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(MemberAPI, self).__init__()

    def get(self, id):
        member = [member for member in members if member['id'] == id]
        if len(member) == 0:
            abort(404)
        return {'member': marshal(member[0], member_fields)}

    def put(self, id):
        member = [member for member in members if member['id'] == id]
        if len(member) == 0:
            abort(404)
        member = member[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                member[k] = v
        return {'member': marshal(member, member_fields)}

    def delete(self, id):
        member = [member for member in members if member['id'] == id]
        if len(member) == 0:
            abort(404)
        members.remove(member[0])
        return {'result': True}


api.add_resource(MemberListAPI, '/nostra-plata/api/v1.0/members', endpoint='members')
api.add_resource(MemberAPI, '/nostra-plata/api/v1.0/members/<int:id>', endpoint='member')
