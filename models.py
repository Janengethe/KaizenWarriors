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

class PersonalRecord(db.Model):
    __tablename__ = 'personal_record'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    max_bench_press = db.Column(db.Integer)
    max_deadlift = db.Column(db.Integer)
    max_squat = db.Column(db.Integer)
    date = db.Column(db.Date)
    user = db.relationship(
        'Users', backref=db.backref('personal_records', lazy=True)
        )

class ExerciseLog(db.Model):
    __tablename__ = 'exercise_logs'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    exercise = db.Column(db.String(255))
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    
    
class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    exercise_logs = db.relationship("ExerciseLog", cascade="all, delete-orphan", backref="workout")
    user = db.relationship('Users', backref=db.backref('workouts', lazy=True))

# class Workout(db.Model):
#     __tablename__ = 'workout'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     date = db.Column(db.Date)
#     exercise = db.Column(db.String(255))
#     sets = db.Column(db.Integer)
#     reps = db.Column(db.Integer)
#     weight = db.Column(db.Float)
#     user = db.relationship('Users', backref=db.backref('workouts', lazy=True))


class Packages(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    duration = db.Column(db.Integer)
    memberships = db.relationship('Membership', backref='package', lazy=True)

class Membership(db.Model):
    __tablename__ = 'membership'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    user = db.relationship(
        'Users', backref=db.backref('memberships', lazy=True)
        )

class Checkins(db.Model):
    __tablename__ = 'checkins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    membership_id = db.Column(db.Integer, db.ForeignKey('membership.id'))
    user = db.relationship('Users', backref=db.backref('checkins', lazy=True))
