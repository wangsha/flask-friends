#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from tests.utils import do_invite_return_token_request
from friends.utils import make_token
from friends.frameworks.flask.routes import okay_response
from friends.actions import (
    do_invite_friend,
    reject_friendship_request,
    accept_friendship_request,
)

new_user_headers = {"AUTHORIZATION": "5b5dcf3474f4b9706920e116"}


def test_batch_resource_access_control(app, friends):
    for url in (
        "/friend_requests",
        "/friend_invitations",
        "/friend_requests_rejected",
        "/friendlist",
    ):
        with app.test_client() as c:
            # request with does not exists user
            resp = c.get(url, headers=new_user_headers)
            assert resp.status_code == 401


def test_create_friendship(app, friends, users):
    # request with does not exists user
    resp = _test_create_friendship(
        app, new_user_headers, dict(email="new_user@ff.com", message="")
    )
    assert resp.status_code == 401

    # request with exists user
    user = users[0]
    headers = {"AUTHORIZATION": user.id}
    # miss parameter message
    resp = _test_create_friendship(app, headers, dict(email="new_user@ff.com"))
    assert resp.status_code == 400
    # miss parameter email
    resp = _test_create_friendship(app, headers, dict(message=""))
    assert resp.status_code == 400

    resp = _test_create_friendship(
        app, headers, dict(email="new_user@ff.com", message="")
    )
    assert resp.status_code == 200
    assert resp.data.decode("utf-8") == okay_response()
    resp = _test_create_friendship(app, headers, dict(email=users[1].email, message=""))
    assert resp.status_code == 200
    assert resp.data.decode("utf-8") == okay_response()


def _test_create_friendship(app, headers, post_data):
    url = "/request_friend"
    with app.test_client() as c:
        resp = c.post(url, headers=headers, data=post_data)
        return resp


def test_accept_friend_request(strategy, users, app):
    from_user = users[0]
    to_user = users[1]
    do_invite_friend(strategy, from_user, to_user.email, "Hello!")
    token = make_token(strategy, from_user, to_user)
    url = "/accept/{token}".format(token=token)

    with app.test_client() as c:
        resp = c.get(url)
        assert resp.status_code == 200
        assert resp.data.decode("utf-8") == okay_response()


def test_reject_friend_request(strategy, users, app):
    from_user = users[0]
    to_user = users[1]
    do_invite_friend(strategy, from_user, to_user.email, "Hello!")
    token = make_token(strategy, from_user, to_user)
    url = "/reject/{token}".format(token=token)

    with app.test_client() as c:
        resp = c.get(url)
        assert resp.status_code == 200
        assert resp.data.decode("utf-8") == okay_response()


def test_cancel_friend_request(strategy, users, app):
    from_user = users[0]
    to_user = users[1]
    do_invite_friend(strategy, from_user, to_user.email, "Hello!")
    token = make_token(strategy, from_user, to_user)
    url = "/cancel/{token}".format(token=token)

    with app.test_client() as c:
        resp = c.get(url)
        assert resp.status_code == 200
        assert resp.data.decode("utf-8") == okay_response()


def test_friend_requests(strategy, users, app):
    url = "/friend_requests"

    with app.test_client() as c:
        user = users[0]
        headers = {"AUTHORIZATION": user.id}
        resp = c.get(url, headers=headers)
        data = json.loads(resp.data)
        assert resp.status_code == 200
        assert len(data) == 0
        do_invite_friend(strategy, users[1], user.email, "")
        do_invite_friend(strategy, users[2], user.email, "")
        do_invite_friend(strategy, user, users[3].email, "")
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) == 3


def test_friend_requests_rejected(strategy, users, app):
    url = "/friend_requests_rejected"

    with app.test_client() as c:
        user = users[0]
        headers = {"AUTHORIZATION": user.id}
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) == 0

        token, request = do_invite_return_token_request(strategy, users[1], user)
        reject_friendship_request(strategy, token)
        token, request = do_invite_return_token_request(strategy, users[2], user)
        accept_friendship_request(strategy, token)
        token, request = do_invite_return_token_request(strategy, user, users[3])
        reject_friendship_request(strategy, token)
        token, request = do_invite_return_token_request(strategy, user, users[4])
        accept_friendship_request(strategy, token)
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) == 2


def test_friend_invitations(strategy, app, users):
    url = "/friend_invitations"

    with app.test_client() as c:
        user = users[0]
        headers = {"AUTHORIZATION": user.id}
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) == 0
        do_invite_friend(strategy, user, users[1].email, "Hi!")
        do_invite_friend(strategy, user, "aa@ff.com", "Hi!")
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) == 1
        assert data[0]["to_user_email"] == "aa@ff.com"


def test_remove_friend(strategy, app, users):
    from_user = users[0]

    with app.test_client() as c:
        token = make_token(strategy, from_user, users[1])
        url = "/remove/{token}".format(token=token)
        resp = c.get(url)
        assert resp.status_code == 200

        strategy.storage.friends.create(from_user, user2=users[1])
        token = make_token(strategy, from_user, users[1])
        url = "/remove/{token}".format(token=token)
        resp = c.get(url)
        assert resp.status_code == 200


def test_friends(strategy, app, users):
    url = "/friendlist"
    from_user = users[0]
    headers = {"AUTHORIZATION": from_user.id}

    with app.test_client() as c:
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data == []

        strategy.storage.friends.create(from_user, user2=users[1])
        strategy.storage.friends.create(from_user, user2=users[2])
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) == 2
