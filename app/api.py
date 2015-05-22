#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

from app import app
from .models import User, Group, Loan

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

loan_fields = {
    'id': fields.Integer,
    'creditor_id': fields.Integer,
    'debtor_id': fields.Integer,
    'group_id': fields.Integer,
    'amount': fields.Integer,
}

class GroupMembersAPI(Resource):

    def get(self, id):
        members = Group.query.get(id).members
        return {'members': marshal(members, member_fields)}

class LoansGivenAPI(Resource):

    def get(self, creditor_id):
        loans_given = Loan.query.filter_by(creditor_id=creditor_id).all()
        total = 0
        for loan in loans_given:
            total += loan.amount

        return {'loans_given': marshal(loans_given, loan_fields), 'total': total}

class LoansGottenAPI(Resource):

    def get(self, debtor_id):
        loans_gotten = Loan.query.filter_by(debtor_id=debtor_id).all()
        total = 0
        for loan in loans_gotten:
            total += loan.amount

        return {'loans_gotten': marshal(loans_gotten, loan_fields), 'total': total}

api.add_resource(GroupMembersAPI, '/nostra-plata/api/v1.0/group-members/<int:id>', endpoint='group-members')
api.add_resource(LoansGivenAPI, '/nostra-plata/api/v1.0/loans-given/<int:creditor_id>', endpoint='loans-given')
api.add_resource(LoansGottenAPI, '/nostra-plata/api/v1.0/loans-gotten/<int:debtor_id>', endpoint='loans-gotten')
