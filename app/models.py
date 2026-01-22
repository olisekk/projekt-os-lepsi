from . import db

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Query {self.city}>"
