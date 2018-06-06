# -*- coding: utf-8 -*-

from flask import Blueprint, g, request
from werkzeug.exceptions import abort

from friends.actions import do_invite_friend, \
    accept_friendship_request, reject_friendship_request, cancel_friendship_request, \
    friendship_request_list, friendship_request_list_rejected, friendship_invitation_list, \
    friendlist, delete_friend
from friends.frameworks.flask.utils import load_strategy

friends_blueprint = Blueprint('friends', __name__)


def okay_response():
    resp = """
    <!DOCTYPE html>
<html lang="en">
<title>Success</title>
<meta name="viewport" content="width=device-width">

<head>
    <meta charset="utf-8">
    <title>Ok</title>
    <style>
        ::-moz-selection {
        background: #b3d4fc;
        text-shadow: none;
        }

        ::selection {
        background: #b3d4fc;
        text-shadow: none;
        }

        html {
        padding: 30px 10px;
        font-size: 20px;
        line-height: 1.4;
        color: #737373;
        background: #f0f0f0;
        -webkit-text-size-adjust: 100%;
        -ms-text-size-adjust: 100%;
        }

        html,
        input {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }

        body {
        max-width: 500px;
        _width: 500px;
        padding: 30px 20px 50px;
        border: 1px solid #b3b3b3;
        border-radius: 4px;
        margin: 0 auto;
        box-shadow: 0 1px 10px #a7a7a7, inset 0 1px 0 #fff;
        background: #fcfcfc;
        }

        h1 {
        margin: 0 10px;
        font-size: 50px;
        text-align: center;
        }

        h1 span {
        color: #bbb;
        }

        h3 {
        margin: 1.5em 0 0.5em;
        }

        .container {
        max-width: 380px;
        _width: 380px;
        margin: 0 auto;
        }



    </style>
</head>
<body>
<div class="container">
    <h1>Ok <span>:)</span></h1>
    <h3>Your request has been recorded.</h3>
</div>
</body>
</html>
    """
    return resp


@friends_blueprint.route('/request_friend', methods=('POST',))
@load_strategy
def create_friendship():
    try:
        user = g.strategy.authenticate_request(request.headers.get('AUTHORIZATION', None))
        if not user:
            abort(401)

        email = request.form['email'] if request.form else request.json['email']
        message = request.form['message'] if request.form else request.json['message']

        do_invite_friend(g.strategy,
                         from_user=user,
                         to_user_email=email,
                         message=message)
        return okay_response(), 200

    except Exception as e:
        return e.message, e.code


@friends_blueprint.route('/accept/<string:token>', methods=('GET',))
@load_strategy
def accept_friend_request(token):
    try:
        accept_friendship_request(g.strategy, token)
        return okay_response(), 200
    except Exception as e:
        return e.message, e.code


@friends_blueprint.route('/reject/<string:token>', methods=('GET',))
@load_strategy
def reject_friend_request(token):
    try:
        reject_friendship_request(g.strategy, token)
        return okay_response(), 200
    except Exception as e:
        return e.message, e.code


@friends_blueprint.route('/cancel/<string:token>', methods=('GET',))
@load_strategy
def cancel_friend_request(token):
    try:
        cancel_friendship_request(g.strategy, token)
        return okay_response(), 200
    except Exception as e:
        return e.message, e.code


@friends_blueprint.route('/friend_invitations', methods=('GET',))
@load_strategy
def friend_invitations():
    user = g.strategy.authenticate_request(request.headers.get('AUTHORIZATION', None))
    if not user:
        abort(401)
    res = friendship_invitation_list(g.strategy, user)
    return g.strategy.make_response(res)


@friends_blueprint.route('/friend_requests', methods=('GET',))
@load_strategy
def friend_requests():
    user = g.strategy.authenticate_request(request.headers.get('AUTHORIZATION', None))
    if not user:
        abort(401)
    res = friendship_request_list(g.strategy, user)
    return g.strategy.make_response(res)


@friends_blueprint.route('/friend_requests_rejected', methods=('GET',))
@load_strategy
def friend_requests_rejected():
    user = g.strategy.authenticate_request(request.headers.get('AUTHORIZATION', None))
    if not user:
        abort(401)
    res = friendship_request_list_rejected(g.strategy, user)
    return g.strategy.make_response(res)


@friends_blueprint.route('/friendlist', methods=('GET',))
@load_strategy
def friends():
    user = g.strategy.authenticate_request(request.headers.get('AUTHORIZATION', None))
    if not user:
        abort(401)
    res = friendlist(g.strategy, user)
    return g.strategy.make_response(res)


@friends_blueprint.route('/remove/<string:token>', methods=('GET',))
@load_strategy
def remove_friend(token):
    try:
        delete_friend(g.strategy, token)
        return okay_response(), 200
    except Exception as e:
        return e.message, e.code
