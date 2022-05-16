from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from personal_blog.models import User



class RegistrationForm(FlaskForm):
    username= StringField('Username',
                          validators=[DataRequired(),Length(min=4,max=20)])
    email= StringField('email',
                       validators=[DataRequired(),Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',
                       validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Signup')
    
    # user authentication
    def validate_username(self, username):
       
          user = User.query.filter_by(username=username.data).first()
          if user:
             raise ValidationError('The username is already taken ') 

    def validate_email(self, email):
        
          user = User.query.filter_by(email=email.data).first()
          if user:
            raise ValidationError('The email is already taken ') 


class LoginForm(FlaskForm):
    
    email= StringField('email',
                       validators=[DataRequired(),Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    remember= BooleanField('Remember Me')
    submit= SubmitField('Log In')