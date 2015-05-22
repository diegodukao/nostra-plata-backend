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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    loans_given = db.relationship('Loan', backref=db.backref('creditor'),
                              primaryjoin=id==Loan.creditor_id)
    loans_gotten = db.relationship('Loan', backref=db.backref('debtor'),
                               primaryjoin=id==Loan.debtor_id)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    members = db.relationship('User', secondary=group_members,
                    backref=db.backref('groups', lazy='dynamic'))

    def __repr__(self):
        return '<Group %r>' % (self.name)

