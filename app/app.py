import os

from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from model_interactions import *
auth = HTTPBasicAuth()
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'blapi.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '\x19\xffDM\xbd\x12\x02\xf1\x90ZR\x16`\xfc\x13\xa7^7b\\\x8d5%\x12'
db = SQLAlchemy(app)


@app.errorhandler(404)
def bucketlist_not_found(error):
    return jsonify({'message': 'Bucket List Not Found'})


@app.route('/auth/register', methods=['POST'])
def register_new_user():
    return jsonify({'message': 'I got the request'})


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.json['username']
    return jsonify({'message': 'Hello {0}'.format(username)})


@app.route('/bucketlists', methods=['POST'])
@auth.login_required
def create_bucket_list(self):
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
