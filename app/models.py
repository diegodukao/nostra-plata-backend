from app import db

group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    members = db.relationship('User', secondary=group_members,
                    backref=db.backref('groups', lazy='dynamic'))

    def __repr__(self):
        return '<Group %r>' % (self.name)
