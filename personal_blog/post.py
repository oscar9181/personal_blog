from flask import Flask,render_template
from forms import RegistrationForm,LoginForm
app = Flask(__name__)

app.config['SECRET_KEY']='40d3625a'

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

@app.route("/register")
def register():
    form=RegistrationForm
    return render_template('register.html',title='Register',form=form)


@app.route("/login")
def login():
    form=LoginForm
    return render_template('login.html',title='Login',form=form)


if __name__== '__main__':
     app.run(debug = True)