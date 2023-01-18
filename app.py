import os
from flask import Flask, request, redirect, url_for, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import current_user, login_required, login_user, logout_user, LoginManager

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Users
import helpers
from forms import LoginForm, RegisterForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please, Login to continue'


@login_manager.user_loader
def load_user(users_id):
    """Locate user by id"""
    return Users.query.get(int(users_id))

app.url_map.strict_slashes = False

@app.route('/')
def index():
    return ("Hello Home!")

@app.route('/register', methods=['GET', 'POST'])
def register():
    uin = helpers.logged_in(current_user)

    form = RegisterForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        password=form.password.data
        role=form.role.data
        
        new_user = Users(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('New user {} with email {} created successfully.'.format(name, email))
        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('register.html', uin=uin, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Welcome {}!'.format(email))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('See you later!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
