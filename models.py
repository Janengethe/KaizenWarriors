from app import db
from sqlalchemy.dialects.postgresql import ENUM
import bcrypt

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

class Users(db.Model):
    __tablename__ = 'users'

    role_enum = ENUM('Owner', 'Member', name='role_enum')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(role_enum, nullable=False)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return self.password

# class Users(db.Model):
#     __tablename__ = 'users'

#     role_enum = ENUM('Owner', 'Member', name='role_enum')
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     email = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))
#     role = db.Column(role_enum, nullable=False)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))
#     role = db.Column(db.Enum('owner', 'member', name='role_enum'))
#     member = db.relationship("Member", uselist=False, back_populates="user")
    
# class Member(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     date_joined = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship("User", back_populates="member")
