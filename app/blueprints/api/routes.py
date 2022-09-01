from . import api
from .auth import basic_auth, token_auth
from flask import jsonify, request
from app.models import Post, User

# @api.route('/')
# def index():
#     names = ['Amanda','Bob','Carl']
#     return jsonify(names)

@api.route('/token')
@basic_auth.login_required # this is coming from our auth.py file, requires you to be authenticated
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({"token": token, "token_expiration": user.token_expiration})


@api.route('/posts', methods=["GET"])
def posts():
    posts = Post.query.all()
    # return jsonify(posts) #this won't work because Python objects are not jsonifiable. Make a function in models.py that will make it into a dictionary or a string
    return jsonify([p.to_dict() for p in posts])


@api.route('/posts/<post_id>')
def get_posts(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@api.route('/posts', methods=["POST"])
@token_auth.login_required
# ^ makes it so that you can't post stuff to the api without verified user
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json!!!'}), 400
    # get the data from the request body
    data = request.json
    # print(data, type(data))
    # validate the data
    # for field in ['title','body','user_id']: # instead of user id we'll just use whoever is logged in
    for field in ['title','body']:
        if field not in data:
            # if field is not in the request body, respond with a 400 error
            return jsonify({'error': f"'{field}' must be in request body"}), 400

    title = data.get('title')
    body = data.get('body')
    user_id= token_auth.current_user().user_id
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201



@api.route('/users', methods=['POST'])
def post_user():
    # return 'create user'
    if not request.is_json: # check if the request is in the valid format ('request' is imported from flask!!)
        return jsonify({"error": "Your request content-type must be application/json!!!"}), 400 # the 400 is an error code

    # if it is in the valid format, it will continue to below:
    data = request.json
    # check that the data is being submitted in the right format (otherwise, return an error and a 400 code)
    for field in ['email','username','password']:
        if field not in data: 
            return jsonify({"error": f"'{field}' must be in request body"}), 400
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({"error": "User with username and/or email already exists"}), 400
    return jsonify(User(email=email, username=username, password=password).to_dict()), 201


@api.route('/users',methods=['GET'])
def get_users():
    users = User.query.all()
    # Make a function in models.py that will make it into a dictionary so that it's jsonifiable
    return jsonify([u.to_dict() for u in users])


@api.route('/users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())