import os
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

from flask import Flask, jsonify, abort, request, g
from flask_httpauth import HTTPTokenAuth
from sqlalchemy.orm import sessionmaker
from models.models import Base, engine, User


auth = HTTPTokenAuth(scheme='Token')
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config[
    'SECRET_KEY'] = '\x19\xffDM\xbd\x12\x02\xf1\x90ZR\x16`\xfc\x13\xa7^7b\\\x8d5%\x12'
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@auth.verify_token
def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        # The token is valid but has expired
        return None
    except BadSignature:
        # The token is invalid
        return None
    user_id = data['id']
    return user_id


@app.errorhandler(404)
def bucketlist_not_found(error):
    return jsonify({'message': 'Bucket List Not Found'})


def verify_password(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.current_user = user
    return True


@app.route('/auth/register', methods=['POST'])
def register_new_user():
    username = request.json.get('username')
    password = request.json.get('password')

    # Check if username | password are provided
    if username is None or password is None:
        return jsonify({'message': 'Username/Password Not Provided!'})

    # Check if the username already exists
    if session.query(User).filter_by(username=username).first() is not None:
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message': 'User already exists!'})
        # Status Code: 201 -> Test This

    user = User(username=username)
    user.hash_password(password)
    session.add(user)

    try:
        session.commit()
    except Exception:
        session.rollback()
        return jsonify({'message': 'Error occured while adding user!'})
    return jsonify({'user': user.username})
    # Status Code: 200 -> Test This


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if verify_password(username, password):
        token = g.current_user.generate_auth_token()
        return jsonify({
            'message': 'Hello, {0}'.format(g.current_user.username),
            'token': token.decode('ascii')
            })
    else:
        return jsonify({'message': 'Invalid Username/Password'})


@app.route('/bucketlists', methods=['POST'])
@auth.login_required
def create_bucket_list():
    return jsonify({'message': 'Creating Bucket List'})


@app.route('/bucketlists', methods=['GET'])
@auth.login_required
def get_bucket_lists():
    return jsonify({'message': 'I got here!'})


@app.route('/bucketlists/<int:id>', methods=['GET'])
@auth.login_required
def get_specific_bucket_list(id):
    return jsonify({'id': id})


@app.route('/bucketlists/<int:id>', methods=['PUT'])
@auth.login_required
def update_bucket_list(id):
    return jsonify({'id': id})


@app.route('/bucketlists/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_bucket_list(id):
    return jsonify({'id': id})


@app.route('/bucketlists/<int:id>/items', methods=['POST'])
@auth.login_required
def add_bucket_list_item(id):
    return jsonify({'id': id})


@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_bucket_list_item(id, item_id):
    return jsonify({'id': id, 'item_id': item_id})


@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_bucket_list_item(id, item_id):
    return jsonify({'id': id, 'item_id': item_id})


if __name__ == '__main__':
    app.run(debug=True)
