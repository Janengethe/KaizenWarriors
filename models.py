from app import db

class About(db.Model):
    __tablename__ = 'about'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    about = db.Column(db.String())

    def __init__(self, name, about):
        self.name = name
        self.about = about

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'about':self.about
        }
