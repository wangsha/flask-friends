# -*- coding: utf-8 -*-

from flask import Blueprint, g, request, jsonify
from werkzeug.exceptions import abort

from friends.actions import do_invite_friend, \
    accept_friendship_request, reject_friendship_request, cancel_friendship_request, \
    friendship_request_list, friendship_request_list_rejected
from friends.frameworks.flask.utils import load_strategy


friends_blueprint = Blueprint('friends', __name__)


@friends_blueprint.route('/request_friend', methods=('POST',))
@load_strategy
def create_friendship():
    email = request.form['email']
    user = g.strategy.authenticate_request(request.headers['Authenticate'])
    if not user:
        abort(401)

    do_invite_friend(g.strategy,
                     from_user=user,
                     to_user_email=email,
                     message=request.data['message'])

    return 'Ok', 200


@friends_blueprint.route('/accept/<string:token>', methods=('POST',))
@load_strategy
def accept_friend_request(token):
    accept_friendship_request(g.strategy, token)
    return 'Ok', 200


@friends_blueprint.route('/reject/<string:token>', methods=('POST',))
@load_strategy
def reject_friend_request(token):
    reject_friendship_request(g.strategy, token)
    return 'Ok', 200


@friends_blueprint.route('/cancel/<string:token>', methods=('POST',))
@load_strategy
def cancel_friend_request(token):
    cancel_friendship_request(g.strategy, token)
    return 'Ok', 200


@friends_blueprint.route('/friend_requests', methods=('GET',))
@load_strategy
def friend_requests():
    user = g.strategy.authenticate_request(request.headers['Authenticate'])
    res = friendship_request_list(g.strategy, user)
    return jsonify(res)


@friends_blueprint.route('/friend_requests_rejected', methods=('GET',))
@load_strategy
def friend_requests_rejected():
    user = g.strategy.authenticate_request(request.headers['Authenticate'])
    res = friendship_request_list_rejected(g.strategy, user)
    return jsonify(res)
