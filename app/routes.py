from app import app1
from flask import render_template

@app1.route('/')
def index():
    user_info = {
        'username':'mariapan',
        'email':'maria.pan0330@gmail.com'
    }
    colors = ['red','orange','gold','green','blue','purple']
    return render_template('index.html', user=user_info, colors=colors)
    # render_template takes in any number of arguments BY KEYWORD


@app1.route('/signup')
def signup():
    return render_template('signup.html')