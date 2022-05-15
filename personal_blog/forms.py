from operator import eq
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo


class RegistrationForm(FlaskForm):
    username= StringField('Username',
                          validators=[DataRequired(),Length(min=4,max=20)])
    email= StringField('email',
                       validators=[DataRequired(),Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',
                       validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Signup')