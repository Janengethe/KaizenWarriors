import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import About, Users

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/name/<name>")
def get_name(name):
    return "name : {}".format(name)

@app.route("/details")
def get_details():
    name=request.args.get('name')
    about=request.args.get('about')
    return "Name : {}, About: {}".format(name,about)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         role = request.form['role']
#         new_user = User(name=name, email=email, password=password, role=role)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('You are registered!')
#         return redirect(url_for('login'))
#     return render_template('register.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         role = request.form['role']

#         new_user = Users(name=name, email=email, role=role)
#         new_user.password = new_user.password = new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({'message': 'New user created successfully.'}), 201
#     return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # check if email already exists
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400
        
        # check if the password is strong
        if not is_strong_password(password):
            return jsonify({'error': 'Password is not strong'}), 400
        
        new_user = Users(name=name, email=email, role=role)
        new_user.password = new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created successfully.'}), 201
    return render_template('register.html')

def is_strong_password(password):
    """
    Function to check if a password is strong enough
    """
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    return True


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
