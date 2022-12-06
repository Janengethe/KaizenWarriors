import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import About

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
