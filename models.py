from app import db
from werkzeug.security import generate_password_hash
from sqlalchemy.dialects.postgresql import ENUM
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    role_enum = ENUM('Owner', 'Member', name='role_enum')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(role_enum, nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        self.name = ""
        self.email = ""
        self.password = ""
        self.role = ""

        for k, v in kwargs.items():
            if k == 'password':
                Users.__set_password(self, v)
            else:
                setattr(self, k, v)

    def __set_password(self, password: str) -> None:
        """
            Encrypts password
        """
        secure_pw = generate_password_hash(password)
        setattr(self, 'password', secure_pw)
