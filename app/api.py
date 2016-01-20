#!flask/bin/python
from flask import jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from app import app, db
from .models import Group, Loan, User

api = Api(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'name': fields.String,
}

group_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

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


class UserAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, required=True,
            help="Username can't be null", location='json')
        self.reqparse.add_argument("password", type=str, required=True,
            help="Password can't be null", location='json')
        self.reqparse.add_argument("name", type=str, required=False)
        super(UserAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        user = User(
            username=args['username'],
            name=args['name'],
        )
        user.hash_password(args['password'])
        db.session.add(user)
        db.session.commit()

        return {'user': marshal(user, user_fields)}


class GroupAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, required=True,
           help="Group must have a name", location='json')
        super(GroupAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        group = Group(
            name=args['name'],
        )
        db.session.add(group)
        db.session.commit()

        return {'group': marshal(group, group_fields)}


class GroupMembersAPI(Resource):

    def get(self, id):
        members = Group.query.get(id).members
        return marshal(members, member_fields)


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
        self.reqparse = reqparse.RequestParser()
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


api.add_resource(UserAPI, '/api/v1.0/users', endpoint='users')
api.add_resource(GroupAPI, '/api/v1.0/group', endpoint='group')
api.add_resource(GroupMembersAPI, '/api/v1.0/group-members/<int:id>', endpoint='group-members')
api.add_resource(LoansGivenAPI, '/api/v1.0/loans-given/<int:creditor_id>', endpoint='loans-given')
api.add_resource(LoansGottenAPI, '/api/v1.0/loans-gotten/<int:debtor_id>', endpoint='loans-gotten')
api.add_resource(LoanAPI, '/api/v1.0/loan', endpoint='loan')
