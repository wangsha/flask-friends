# -*- coding: utf-8 -*-

import pytest

from mock import call
from utils import make_token
from friends.actions import do_invite_friend, _load_friendship_request,\
    friendship_request_list, accept_friendship_request


def test_do_invite_friend(app, users, strategy):
    from_user = users[0]
    message = 'Hello!'

    # to_user does not exists
    to_user_email = 'idontexist@ff.com'
    do_invite_friend(strategy, from_user=from_user,
                     to_user_email=to_user_email,
                     message=message)
    invitation = strategy.storage.friendInvitation.objects.filter(
        from_user=from_user, to_user_email=to_user_email, message="Hello!"
    ).count() > 0

    # to_user exists
    to_user = users[1]
    do_invite_friend(strategy, from_user=from_user,
                     to_user_email=to_user.email,
                     message=message)
    assert strategy.storage.friendshipRequest.objects.filter(
        from_user=from_user, to_user=to_user, message=message).count() > 0


def test_new_user_created(app, flask_mongoengine_storage):
    pass


def test_load_friendship_request(strategy, users):
    from_user = users[0]
    to_user = users[1]
    do_invite_friend(strategy, from_user=from_user, to_user_email=to_user.email,
                     message="Hello!")
    token = make_token(strategy, from_user, to_user)
    request = _load_friendship_request(strategy, token)
    assert request.from_user == from_user
    assert request.to_user == to_user


def test_accept_friendship_request(strategy, users):
    from_user = users[0]
    to_user = users[1]
    do_invite_friend(strategy, from_user=from_user, to_user_email=to_user.email,
                     message="Hello!")
    token = make_token(strategy, from_user, to_user)

    accept_friendship_request(strategy, token)
    strategy.storage.friendshipRequest.filter(from_user=from_user, to_user=to_user).count() == 0
    strategy.storage.friends.filter(user1=request.from_user, user2=request.to_user).count() == 1


# def test_reject_friendship_request(strategy, token):
#     request = _load_friendship_request(strategy, token)
#     strategy.storage.friendshipRequest.reject(request.id)


# def test_cancel_friendship_request(strategy, token):
#     request = _load_friendship_request(strategy, token)
#     strategy.storage.friendshipRequest.remove(request.id)


def test_friendship_request_list(users, strategy):
    user_a = users[0]
    user_b = users[3]

    # 2 invite to user_a
    do_invite_friend(
        strategy, from_user=users[1], to_user_email=user_a.email, message='')
    do_invite_friend(
        strategy, from_user=users[2], to_user_email=user_a.email, message='')
    res = friendship_request_list(strategy, user_a)
    assert len(res['requesting']) == 0
    assert len(res['requested']) == 2

    # 1 invite from user_a to user_b
    do_invite_friend(
        strategy, from_user=user_a, to_user_email=user_b.email, message='')
    res = friendship_request_list(strategy, user_a)
    assert len(res['requesting']) == 1
    assert len(res['requested']) == 2
    res = friendship_request_list(strategy, user_b)
    assert len(res['requesting']) == 0
    assert len(res['requested']) == 1
