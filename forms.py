#!/usr/bin/env python3
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import DateField, FieldList, FormField, FloatField
from wtforms import StringField, PasswordField, SubmitField, IntegerField,\
    SelectField
from wtforms.validators import Email, EqualTo, Length
from wtforms.validators import InputRequired, ValidationError, DataRequired,\
    NumberRange

from models import Users, Checkins

class RegisterForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            InputRequired(),
            Length(min=2, max=255)
            ]
        )
    email = StringField(
        'Email',
        validators=[
            InputRequired(),
            Email(),
            Length(min=6, max=255)]
        )
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            Length(min=6, max=255)
            ]
        )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            InputRequired(),
            EqualTo('password')
            ]
        )
    role = SelectField(
        'Role',
        choices=[('Member', 'Member')],
        validators=[InputRequired()]
        )
    submit = SubmitField('Register')

    # role = SelectField(
    #     'Role',
    #     choices=[('Owner', 'Owner'), ('Member', 'Member')],
    #     validators=[InputRequired()]
    #     )
    # submit = SubmitField('Register')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Already registered!")
        return

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    # srf_token = HiddenField('CSRF Token')
    submit = SubmitField('Log In')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email not registered!")
        return

class CheckinForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Check In')
    
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email not registered!")
        userid = user.id
        now = datetime.now()
        existing_checkin = Checkins.query.filter_by(user_id=userid).all()
        for m in existing_checkin:
            if m.created_at.date() == now.date():
                raise ValidationError("Member already checked in today!")
        return
    
    
class UpdateMemberForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Update')
    
class PersonalRecordForm(FlaskForm):
    max_bench_press = IntegerField(
        'Max Bench Press',
        validators=[
            DataRequired(),
            NumberRange(min=0, max=1000)
            ]
        )
    max_deadlift = IntegerField(
        'Max Deadlift',
        validators=[
            DataRequired(),
            NumberRange(min=0, max=1000)
            ]
        )
    max_squat = IntegerField(
        'Max Squat',
        validators=[
            DataRequired(),
            NumberRange(min=0, max=1000)
            ]
        )
    submit = SubmitField('Save')

class WorkoutForm(FlaskForm):
    date = DateField('Date')
    submit = SubmitField('Save Workout')

class ExerciseLogForm(FlaskForm):
    exercise = StringField('Exercise')
    sets = IntegerField('Sets')
    reps = IntegerField('Reps')
    weight = FloatField('Weight')
    submit = SubmitField('Save Exercise')

# class ExerciseForm(FlaskForm):
#     exercise = StringField(
#         'exercise',
#         validators=[DataRequired(), Length(min=3, max=255)]
#         )
#     sets = IntegerField('sets', validators=[DataRequired()])
#     reps = IntegerField('reps', validators=[DataRequired()])
#     weight = FloatField('weight', validators=[DataRequired()])

# class WorkoutForm(FlaskForm):
#     date = DateField('date', validators=[DataRequired()])
#     exercises = FieldList(FormField(ExerciseForm), min_entries=8)
#     submit = SubmitField('Add Workout')

class PackageForm(FlaskForm):
    name = StringField('Name')
    price = FloatField('Price')
    duration = IntegerField('Duration')
