from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
