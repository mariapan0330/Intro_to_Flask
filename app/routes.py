from app import app
from flask import render_template
from app.forms import SignUpForm

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
        print(form.email.data, form.username.data, form.password.data)
        # the .data prints out whatever they submitted
    return render_template('signup.html', form=form)