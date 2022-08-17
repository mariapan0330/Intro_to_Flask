from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, PostForm
from app.models import User, Post

@app.route('/')
def index():
    user_info = {
        'username':'mariapan',
        'email':'maria.pan0330@gmail.com'
    }
    colors = ['red','orange','gold','green','blue','purple']
    return render_template('index.html', user=user_info, colors=colors)
    # render_template takes in any number of arguments BY KEYWORD


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm() # but you have to use a secret key!
    # if the form is submitted and all the data is valid
    if form.validate_on_submit(): # will return True or False
        # if this doesn't work, it might be because you forgot csrf token.
        print("Form has been successfully validated!!! Yay.")
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # the .data is whatever they submitted
        # Check if that username or email already exists.
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('A user with that username or email already exists.', 'danger')
            return redirect(url_for('signup'))

        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.", 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/create', methods=['GET','POST'])
def create():
    form = PostForm()
    if form.validate_on_submit():
        # get the data!
        title = form.title.data
        body = form.body.data
        new_post = Post(title=title, body=body, user_id=1)
        flash(f'{new_post.title} has been created', 'success')
        return redirect(url_for('index'))
        
    return render_template('createpost.html', form=form)