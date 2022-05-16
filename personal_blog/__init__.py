from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from personal_blog.forms import RegistrationForm,LoginForm


app = Flask(__name__)
app.config['SECRET_KEY']='40d3625a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from personal_blog import post