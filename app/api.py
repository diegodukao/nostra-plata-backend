#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

from app import app
from .models import User, Group

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

member_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

class GroupMembersAPI(Resource):

    def get(self, id):
        members = Group.query.get(id).members
        return {'members': marshal(members, member_fields)}

api.add_resource(GroupMembersAPI, '/nostra-plata/api/v1.0/group-members/<int:id>', endpoint='group-members')
