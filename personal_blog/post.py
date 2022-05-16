from flask import render_template,url_for, flash,redirect
from personal_blog import app
from personal_blog.models import User,Post
from personal_blog.forms import RegistrationForm,LoginForm

posts = [
   {
    'author' :'Sophie Paxton',
    'title'  :'Interface Design',
    'content'  :'Animation is like cursing. If you overuse it, it loses all its impact.',
    'date_posted' : 'October 17 2002'
   }]

@app.route("/")
@app.route("/home")
def home():
    """
    View root page function that returns the home page and its data
    """
    return render_template('home.html',posts=posts)

@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form. validate_on_submit():
        flash('Your account hass been created!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form. validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

