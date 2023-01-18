#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField
from wtforms.validators import Email, EqualTo, Length
from wtforms.validators import InputRequired, ValidationError

from models import Users

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=6, max=255)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=255)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Owner', 'Owner'), ('Member', 'Member')], validators=[InputRequired()])
    # role = StringField('Role',validators=[InputRequired(), Length(min=6, max=255)])
    submit = SubmitField('Register')

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