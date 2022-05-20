import os
import json
import requests
import secrets
from PIL import Image
from flask import render_template,url_for, flash,redirect,request,abort
from personal_blog import app,db,bcrypt
from personal_blog.models import User,Post, Comments,Quote
from personal_blog.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm,CommentForm
from flask_login import login_user,current_user,logout_user,login_required

def get_quote():
    quote_url = 'http://quotes.stormconsultancy.co.uk/random.json'
    req = requests.get(quote_url)
    data = json.loads(req.content)
    quote = Quote(data["quote"],data["author"])
    return quote



@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    quote = get_quote()
    """
    View root page function that returns the home page and its data
    """
    return render_template('home.html',posts=posts,quote=quote)

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  
    form=RegistrationForm()
    if form. validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user= User(username=form.username.data, email=form.email.data,password=hashed_password)  
        db.session.add(user)
        db.session.commit()
        flash('Your account hass been created!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  
    form=LoginForm()
    if form. validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('login unsuccessful.please check email and password','danger')
    return render_template('login.html',title='Login',form=form)
   
@app.route('/logout')
def logout():
    logout_user()
    
    return redirect(url_for('home'))

def save_picture(form_picture):   
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    

    output_size = (100,100)
    i =Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    
    return picture_fn


@app.route('/account',methods=['GET','POST']) 
@login_required
def account():
    form = UpdateAccountForm()
    if form. validate_on_submit():
     if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file =picture_file
        current_user.username =form.username.data
        current_user.email =form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)    
    return render_template('account.html',title='Account',image_file=image_file,form=form)
   


@app.route('/post/new',methods=['GET','POST']) 
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post= Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','success')
        return redirect(url_for('home'))
    return render_template('blogs.html', title='Blogs',form=form,legend='New Blog')


@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_403(post_id)
    if post.author !=current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your blog has been updated')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('blogs.html', title='Update Post',form=form,legend='Update Post')


@app.route('/post/delete/<int:post_id>',methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
    return redirect (url_for('home'))

@app.route("/post/<int:post_id>/comment/new", methods=["POST","GET"])
@login_required
def create_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comments(content=form.content.data,user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted successfully!', 'success')
        return redirect(url_for('post',post_id=post.id))
    return render_template("comment.html", title="post a comment", form=form, legend="Post a comment")
    
    
    
    
        