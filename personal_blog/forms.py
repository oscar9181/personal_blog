from operator import eq
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
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
    
    
class LoginForm(FlaskForm):
    
    email= StringField('email',
                       validators=[DataRequired(),Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    remember= BooleanField('Remember Me')
    submit= SubmitField('Log In')