from passlib.apps import custom_app_context as pwd_context
from app import db

group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creditor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    debtor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    amount = db.Column(db.Integer)

    def __repr__(self):
        return '<Loan: %r to %r: %r>' % (self.creditor.name, self.debtor.name, self.amount)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(120), index=True)
    loans_given = db.relationship('Loan', backref=db.backref('creditor'),
                                  primaryjoin=id == Loan.creditor_id)
    loans_gotten = db.relationship('Loan', backref=db.backref('debtor'),
                                   primaryjoin=id == Loan.debtor_id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    members = db.relationship('User', secondary=group_members,
                    backref=db.backref('groups', lazy='dynamic'))

    def __repr__(self):
        return '<Group %r>' % (self.name)

