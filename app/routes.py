from app import app
from flask import render_template

@app.route('/')
def index():
    user_info = {
        'username':'mariapan',
        'email':'maria.pan0330@gmail.com'
    }
    colors = ['red','orange','gold','green','blue','purple']
    return render_template('index.html', user=user_info, colors=colors)
    # render_template takes in any number of arguments BY KEYWORD


@app.route('/test')
def test():
    return render_template('test.html')