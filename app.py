import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, session,\
    flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import current_user, login_required, login_user, logout_user,\
    LoginManager

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Users, Membership, Packages, Checkins, Workout,\
    PersonalRecord
import helpers
from forms import LoginForm, RegisterForm, PersonalRecordForm, WorkoutForm

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

@app.route('/dashboard')
@login_required
def dashboard():
    member = Users.query.filter_by(id=current_user.id).first()
    return render_template('dashboard.html', member=member)

@app.route('/users')
@login_required
def get_users():
    if current_user.role != "Owner":
        return "You are not authorized to view this page."
    else:
        users = Users.query.all()
        return render_template('users.html', users=users)

@app.route('/add_personal_record', methods=['GET', 'POST'])
@login_required
def add_personal_record():
    form = PersonalRecordForm()
    if form.validate_on_submit():
        # Create a new personal record
        new_personal_record = PersonalRecord(
            max_bench_press=form.max_bench_press.data,
            max_deadlift=form.max_deadlift.data,
            max_squat=form.max_squat.data,
            date=datetime.now(),
            user_id=current_user.id
        )
        db.session.add(new_personal_record)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_personal_record.html', form=form)


@app.route('/view_personal_records')
@login_required
def view_personal_records():
    pr = PersonalRecord.query.filter_by(user_id=current_user.id).all()
    return render_template('personal_records.html', pr=pr)

@app.route('/workout', methods=['GET','POST'])
def create_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        workouts = []
        for workout in form.exercises.data:
            new_workout = Workout(
                user_id=user.id,
                date=form.date.data,
                exercise=workout['exercise'],
                sets=workout['sets'],
                reps=workout['reps'],
                weight=workout['weight']
                )
            db.session.add(new_workout)
            workouts.append(new_workout)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('workout_form.html', form=form)


@app.route('/checkin', methods=['GET', 'POST'])
@login_required
def checkin():
    if request.method == 'POST':
        # handle check-in form submission
        workout = request.form['workout']
        date = datetime.now()
        new_checkin = Checkins(
            workout=workout,
            date=date,
            user_id=current_user.id
            )
        db.session.add(new_checkin)
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('checkin.html')

@app.route('/cancel_membership')
@login_required
def cancel_membership():
    member = Users.query.filter_by(id=current_user.id).first()
    db.session.delete(member)
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))

@app.route('/purchase_sessions')
@login_required
def purchase_sessions():
    return render_template('purchase_sessions.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('See you later!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
