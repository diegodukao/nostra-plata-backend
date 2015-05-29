#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

from app import app, db
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

class LoanAPI(Resource):

    def __init__(self):
        self.reqparse =reqparse.RequestParser()
        self.reqparse.add_argument('creditor_id', type=int, required=True,
                            help='No creditor_id provided', location='json')
        self.reqparse.add_argument('debtor_id', type=int, required=True,
                            help='No debtor_id provided', location='json')
        self.reqparse.add_argument('group_id', type=int, required=True,
                            help='No group_id provided', location='json')
        self.reqparse.add_argument('amount', type=int, required=True,
                            help='No amount provided', location='json')
        super(LoanAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        loan = Loan(
            creditor_id=args['creditor_id'],
            debtor_id=args['debtor_id'],
            group_id=args['group_id'],
            amount=args['amount']
        )
        db.session.add(loan)
        db.session.commit()

        return {'loan': marshal(loan, loan_fields)}


api.add_resource(GroupMembersAPI, '/api/v1.0/group-members/<int:id>', endpoint='group-members')
api.add_resource(LoansGivenAPI, '/api/v1.0/loans-given/<int:creditor_id>', endpoint='loans-given')
api.add_resource(LoansGottenAPI, '/api/v1.0/loans-gotten/<int:debtor_id>', endpoint='loans-gotten')
api.add_resource(LoanAPI, '/api/v1.0/loan', endpoint='loan')
