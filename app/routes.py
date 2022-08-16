from app import app
from flask import render_template
from app.forms import SignUpForm
from app.models import User

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
        new_user = User(email=email, username=username, password=password)
        print(f"{new_user.username} has been created.")
    return render_template('signup.html', form=form)