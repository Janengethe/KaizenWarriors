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
    PersonalRecord, ExerciseLog, Member
import helpers
from forms import LoginForm, RegisterForm, PersonalRecordForm, WorkoutForm,\
    ExerciseLogForm, PackageForm, UpdateMemberForm, CheckinForm

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
    return render_template("base.html")

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
            flash('Welcome {}!'.format(user.name))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    uin = helpers.logged_in(current_user)

    member = Users.query.filter_by(id=current_user.id).first()
    return render_template('dashboard.html', member=member, uin=uin)

@app.route('/users')
@login_required
def get_users():
    if current_user.role != "Owner":
        return "You are not authorized to view this page."
    else:
        users = Users.query.all()
        return render_template('users.html', users=users)

@app.route('/update_member/<int:id>', methods=['GET', 'POST'])
@login_required
def update_member(id):
    id = current_user.id
    form = UpdateMemberForm()
    if form.validate_on_submit():
        new_member = Member(
            email = form.email.data,
            name = form.name.data,
            phone_number = form.phone_number.data
        )
        db.session.add(new_member)
        db.session.commit()
        flash('Your member details have been updated.', 'success')
        return redirect(url_for('index'))
    return render_template('update_member.html', form=form)

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

@app.route('/workouts', methods=['GET', 'POST'])
def list_workouts():
    workouts = Workout.query.all()
    return render_template('list_workouts.html', workouts=workouts)
    
@app.route('/workouts/new', methods=['GET', 'POST'])
def new_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(date=form.date.data)
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for('list_workouts'))
    return render_template('new_workout.html', form=form)
    
@app.route('/workouts/<int:workout_id>/exercise_logs/new', methods=['GET', 'POST'])
def new_exercise_log(workout_id):
    form = ExerciseLogForm()
    workout = Workout.query.get(workout_id)
    if form.validate_on_submit():
        exercise_log = ExerciseLog(exercise=form.exercise.data, sets=form.sets.data, reps=form.reps.data, weight=form.weight.data, workout=workout)
        db.session.add(exercise_log)
        db.session.commit()
        return redirect(url_for('list_workouts'))
    return render_template('new_exercise_log.html', form=form, workout=workout)


@app.route('/package', methods=['GET', 'POST'])
def package():
    form = PackageForm()
    if request.method == 'POST' and form.validate_on_submit():
        package = Packages(name=form.name.data, price=form.price.data, duration=form.duration.data)
        db.session.add(package)
        db.session.commit()
        print(package)
        return redirect('/package')
    return render_template('package.html', form=form)

@app.route('/checkin', methods=['GET', 'POST'])
@login_required
def checkin():
    form = CheckinForm()
    if form.validate_on_submit():
        checkin = Checkins(user_id=current_user.id, date = form.date.data)
        db.session.add(checkin)
        db.session.commit()
        return ('Checked in successfully')
    return render_template('checkin.html', form=form)

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
