#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import binascii

from utils import do_invite_return_token_request
from friends.utils import make_token
from friends.actions import do_invite_friend, reject_friendship_request, accept_friendship_request


new_user_headers = {'AUTHORIZATION': binascii.hexlify('id1234567890')}


def test_create_friendship(app, friends, users):
    # request with does not exists user
    resp = _test_create_friendship(app, new_user_headers,
                                   dict(email='new_user@ff.com', message=''))
    assert resp.status_code == 401

    # request with exists user
    user = users[0]
    headers = {'AUTHORIZATION': user.id}
    # miss parameter message
    resp = _test_create_friendship(app, headers, dict(email='new_user@ff.com'))
    assert resp.status_code == 400
    # miss parameter email
    resp = _test_create_friendship(app, headers, dict(message=''))
    assert resp.status_code == 400

    resp = _test_create_friendship(app, headers,
                                   dict(email='new_user@ff.com', message=''))
    assert resp.status_code == 200
    resp = _test_create_friendship(app, headers,
                                   dict(email=users[1].email, message=''))
    assert resp.status_code == 200


def _test_create_friendship(app, headers, post_data):
    url = '/request_friend'
    with app.test_client() as c:
        resp = c.post(url, headers=headers, data=post_data)
        return resp


def test_accept_friend_request(strategy, users, app):
    from_user = users[0]
    to_user = users[1]
    do_invite_friend(strategy, from_user, to_user.email, 'Hello!')
    token = make_token(strategy, from_user, to_user)
    url = '/accept/{token}'.format(token=token)

    with app.test_client() as c:
        resp = c.post(url)
        assert resp.status_code == 200


def test_reject_friend_request(strategy, users, app):
    from_user = users[0]
    to_user = users[1]
    do_invite_friend(strategy, from_user, to_user.email, 'Hello!')
    token = make_token(strategy, from_user, to_user)
    url = '/reject/{token}'.format(token=token)

    with app.test_client() as c:
        resp = c.post(url)
        assert resp.status_code == 200


def test_cancel_friend_request(strategy, users, app):
    from_user = users[0]
    to_user = users[1]
    do_invite_friend(strategy, from_user, to_user.email, 'Hello!')
    token = make_token(strategy, from_user, to_user)
    url = '/cancel/{token}'.format(token=token)

    with app.test_client() as c:
        resp = c.post(url)
        assert resp.status_code == 200


def test_friend_requests(strategy, users, app):
    url = '/friend_requests'

    with app.test_client() as c:
        # request with does not exists user
        resp = c.get(url, headers=new_user_headers)
        assert resp.status_code == 401

        # request with exists user
        user = users[0]
        headers = {'AUTHORIZATION': user.id}
        do_invite_friend(strategy, users[1], user.email, '')
        do_invite_friend(strategy, users[2], user.email, '')
        do_invite_friend(strategy, user, users[3].email, '')
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data['requesting']) == 1
        assert len(data['requested']) == 2


def test_friend_requests_rejected(strategy, users, app):
    url = '/friend_requests_rejected'

    with app.test_client() as c:
        # request with does not exists user
        resp = c.get(url, headers=new_user_headers)
        assert resp.status_code == 401

        # request with exists user
        user = users[0]
        headers = {'AUTHORIZATION': user.id}
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['requesting'] == []
        assert data['requested'] == []

        token, request = do_invite_return_token_request(
            strategy, users[1], user)
        reject_friendship_request(strategy, token)
        token, request = do_invite_return_token_request(
            strategy, users[2], user)
        accept_friendship_request(strategy, token)
        token, request = do_invite_return_token_request(
            strategy, user, users[3])
        reject_friendship_request(strategy, token)
        token, request = do_invite_return_token_request(
            strategy, user, users[4])
        accept_friendship_request(strategy, token)
        resp = c.get(url, headers=headers)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data['requesting']) == 1
        assert len(data['requested']) == 1
