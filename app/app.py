from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

from flask import Flask, jsonify, request, g
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
from models import *


auth = HTTPTokenAuth(scheme='Token')
app.config[
    'SECRET_KEY'] = '\x19\xffDM\xbd\x12\x02\xf1\x90ZR\x16`\xfc\x13\xa7^7b\\\x8d5%\x12'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

current_user = {
    'user_id': None
}


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
    current_user['user_id'] = user_id
    return user_id


@app.errorhandler(404)
def bucketlist_not_found(error):
    return jsonify({'message': 'Bucket List Not Found'})


@app.errorhandler(401)
def token_expired_or_invalid(error):
    return jsonify({'message': 'Token Expired/Invalid'})


def verify_password(username, password):
    user = db.session.query(User).filter_by(username=username).first()
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
    if db.session.query(User).filter_by(username=username).first() is not None:
        user = db.session.query(User).filter_by(username=username).first()
        return jsonify({'message': 'User already exists!'})

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'message': 'error occured while adding user'})
    return jsonify({
        'user': user.username,
        'message': 'login endpoint: localhost:5000/auth/login'
    })


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')
    # Check if username | password are provided
    if username is None or password is None:
        return jsonify({'message': 'Username/Password Not Provided!'})

    if verify_password(username, password):
        token = g.current_user.generate_auth_token()
        return jsonify({
            'message': 'Hello, {0}'.format(g.current_user.username),
            'token': token.decode('ascii')
        })
    else:
        return jsonify({'message': 'invalid username/password'})


@app.route('/bucketlists', methods=['POST'])
@auth.login_required
def create_bucket_list():
    user_id = current_user['user_id']
    name = request.json.get('name')

    if name is None:
        return jsonify({'message': 'bucketlist name not provided'})

    if db.session.query(BucketList).filter_by(name=name,
                                              created_by=user_id).first() is not None:
        return jsonify({'message': 'bucketlist already exists'})

    bucketlist = BucketList(name=name, created_by=user_id)
    db.session.add(bucketlist)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'message': 'error occured while creating bucketlist'})

    return jsonify({'message': 'created bucketlist: {0}'.format(name)})


@app.route('/bucketlists', methods=['GET'])
@auth.login_required
def get_bucket_lists():
    user_id = current_user['user_id']
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 2))

    if db.session.query(BucketList).filter_by(created_by=user_id).count() == 0:
        return jsonify({'message': 'no bucketlist found'})

    bucketlist_rows = BucketList.query.filter_by(
        created_by=user_id).paginate(page, limit, False)
    all_pages = bucketlist_rows.pages
    next_page = bucketlist_rows.has_next
    previous_page = bucketlist_rows.has_prev

    if next_page:
        next_page_url = str(request.url_root) + 'bucketlists?' + \
            'limit=' + str(limit) + '&page=' + str(page + 1)
    else:
        next_page_url = None

    if previous_page:
        previous_page_url = str(request.url_root) + '/bucketlists?' + \
            'limit=' + str(limit) + '&page=' + str(page - 1)
    else:
        previous_page_url = None
    bucketlists = []
    for bucketlist in bucketlist_rows.items:
        bucketlists.append({
            'id': bucketlist.bucketlist_id,
            'name': bucketlist.name,
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified,
            'created_by': bucketlist.created_by,
            'total_pages': all_pages,
            'next_page': next_page_url,
            'previous_page': previous_page_url
        })
    return jsonify(bucketlists)


@app.route('/bucketlists/<int:bucketlist_id>', methods=['GET'])
@auth.login_required
def get_specific_bucket_list(bucketlist_id):
    user_id = current_user['user_id']

    if type(bucketlist_id) is not int:
        return jsonify({'message': 'invalid bucketlist id'})

    if db.session.query(BucketList).filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id).all() is None:
        return jsonify({'message': 'bucket list not found'})

    bucketlist_rows = db.session.query(BucketList).filter_by(
        created_by=user_id, bucketlist_id=bucketlist_id).all()
    bucketlists = []
    bucketlistitems = []
    bucketlistitem_rows = db.session.query(BucketListItems).filter_by(
        bucketlist_id=bucketlist_id).all()
    for bucketlistitem in bucketlistitem_rows:
        bucketlistitems.append({
            'id': bucketlistitem.item_id,
            'name': bucketlistitem.name,
            'date_created': bucketlistitem.date_created,
            'date_modified': bucketlistitem.date_modified,
            'done': bucketlistitem.done
        })
    for bucketlist in bucketlist_rows:
        bucketlists.append({
            'id': bucketlist.bucketlist_id,
            'name': bucketlist.name,
            'items': bucketlistitems,
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified,
            'created_by': bucketlist.created_by
        })

    return jsonify(bucketlists)


@app.route('/bucketlists/<int:bucketlist_id>', methods=['PUT'])
@auth.login_required
def update_bucket_list(bucketlist_id):
    user_id = current_user['user_id']
    name = request.json.get('name')

    if name is None:
        return jsonify({'messsage': 'please provide a name'})

    if db.session.query(BucketList).filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id).first() is None:
        return jsonify({'message': 'bucketlist does not exist'})

    bucketlist = db.session.query(BucketList).filter_by(
        bucketlist_id=bucketlist_id, created_by=user_id).first()
    bucketlist.name = name
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'message': 'error updating bucketlist'})
    return jsonify({
        'message': 'bucketlist {0} update successfully'.format(bucketlist_id)})


@app.route('/bucketlists/<int:bucketlist_id>', methods=['DELETE'])
@auth.login_required
def delete_bucket_list(bucketlist_id):
    user_id = current_user['user_id']

    if db.session.query(BucketList).filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id) is None:
        return jsonify({'message': 'bucketlist not found'})

    db.session.query(BucketList).filter_by(
        bucketlist_id=bucketlist_id, created_by=user_id
    ).delete()
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'message': 'error deleting bucketlist'})
    return jsonify({'message':
                    'successfully deleted bucketlist {0}'.format(bucketlist_id)})


@app.route('/bucketlists/<int:bucketlist_id>/items', methods=['POST'])
@auth.login_required
def add_bucket_list_item(bucketlist_id):
    user_id = current_user['user_id']
    name = request.json.get('name')
    done = request.json.get('done', False)

    if name is None:
        return jsonify({'message': 'please provide the name field'})

    if db.session.query(BucketList).filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id) is None:
        return jsonify({'message': 'bucketlist not found'})

    bucketlistitem = BucketListItems(bucketlist_id=bucketlist_id,
                                     name=name, done=done)
    db.session.add(bucketlistitem)

    try:
        db.session.commit()
    except Exception as exc:
        print(exc)
        db.session.rollback()
        return jsonify({'message': 'error adding bucketlist item'})
    return jsonify({'message':
                    'successfully added item {0}'.format(name)})


@app.route('/bucketlists/<int:bucketlist_id>/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_bucket_list_item(bucketlist_id, item_id):
    user_id = current_user['user_id']
    done = request.json.get('done')

    if done is None:
        return jsonify({'message': 'please provide the done field'})

    # Check if the current user owns this bucket list
    if db.session.query(BucketList).filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id) is None:
        return jsonify({'message': 'bucketlist not found'})

    # Check if the bucket list item exists
    if db.session.query(BucketListItems).filter_by(item_id=item_id) is None:
        return jsonify({'message': 'bucket list item not found'})

    # if db.session.query(BucketListItems).filter_by(name=name) is not None:
    #     return jsonify({'message': 'bucket list item already exists'})

    bucketlistitem = db.session.query(BucketListItems).filter_by(
        item_id=item_id).first()
    name = request.json.get('name', bucketlistitem.name)
    bucketlistitem.name = name
    bucketlistitem.done = done

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'message': 'error updating bucket list item'})
    return jsonify({'message': 'successfully updated bucket list item'})


@app.route('/bucketlists/<int:bucketlist_id>/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_bucket_list_item(bucketlist_id, item_id):
    user_id = current_user['user_id']

    if db.session.query(BucketList).filter_by(
            bucketlist_id=bucketlist_id, created_by=user_id).first() is None:
        return jsonify({'message': 'bucketlist not found'})

    if db.session.query(BucketListItems).filter_by(item_id=item_id) is None:
        return jsonify({'message': 'bucketlist item does not exist'})

    db.session.query(BucketListItems).filter_by(
        item_id=item_id
    ).delete()
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'message': 'error deleting bucketlist item'})
    return jsonify({'message': 'successfully deleted bucketlist item'})


if __name__ == '__main__':
    app.run(debug=True)
