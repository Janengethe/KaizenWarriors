import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import About, User

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        new_user = User(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created successfully.'}), 201
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
