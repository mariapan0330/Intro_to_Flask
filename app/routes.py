from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, PostForm, LoginForm
from app.models import User, Post

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)
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
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        # get the data!
        title = form.title.data
        body = form.body.data
        new_post = Post(title=title, body=body, user_id=current_user.user_id)
        flash(f"Posting your article, '{new_post.title}' by {current_user.username}", 'success')
        return redirect(url_for('index'))
        
    return render_template('createpost.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    # validate by checking through existing users and seeing if the one trying to login is one of them
    # and also check if their pw is correct which is saved in our db as a hashed code thing
    # which we have to unscramble using the check password hash method
    if form.validate_on_submit():
        # get username and password from form
        username = form.username.data
        password = form.password.data
        # query the user table for a user with the same username as entered in form
        user = User.query.filter_by(username=username).first()
        # if the user exists
        if user is not None and user.check_password(password):
            # log the user in using the flask-login login_user fn
            login_user(user)
            # flash success message
            flash(f'Login successful! Welcome back, {user.username}.', 'success')
            return redirect(url_for('index'))
        # if username or pw incorrect
        else:
            flash('Incorrect username and/or password. Please try again.','danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out.", 'success')
    return redirect(url_for('index'))


@app.route('/posts/<post_id>')
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<post_id>/edit', methods=["GET","POST"])
@login_required
def edit_post(post_id):
    post_to_edit = Post.query.get_or_404(post_id)
    # make sure the post to edit is owned by the current user
    if post_to_edit.author != current_user:
        flash('You do not have permission to edit this post.', 'danger')
        return redirect(url_for('view_post',post_id=post_id))
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        flash(f"Posting your article, '{post_to_edit.title}' by {current_user.username}", 'success')
        post_to_edit.update(title=title,body=body)
        return redirect(url_for('view_post', post_id=post_id))
    return render_template('editpost.html', post=post_to_edit, form=form)


@app.route('/posts/<post_id>/delete', methods=["GET","POST"])
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    if post_to_delete.author != current_user:
        flash('You do not have permission to delete this post.','danger')
        return redirect(url_for('view_post',post_id=post_id))
    post_to_delete.delete()
    flash(f'{post_to_delete.title} has been deleted.', 'info')
    return redirect(url_for('index'))