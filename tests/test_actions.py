# -*- coding: utf-8 -*-

from utils import do_invite_return_token_request
from friends.actions import do_invite_friend, friendship_request_list,\
    accept_friendship_request, new_user_created, reject_friendship_request,\
    cancel_friendship_request, friendlist, friendship_request_list_rejected


def test_do_invite_friend(app, users, friends):
    strategy = friends.get_strategy()
    from_user = users[0]
    message = 'Hello!'

    # to_user does not exists
    to_user_email = 'idontexist@ff.com'
    do_invite_friend(strategy, from_user=from_user,
                     to_user_email=to_user_email,
                     message=message)
    strategy.storage.friendInvitation.objects.filter(
        from_user=from_user, to_user_email=to_user_email, message="Hello!"
    ).count() > 0

    # to_user exists
    to_user = users[1]
    do_invite_friend(strategy, from_user=from_user,
                     to_user_email=to_user.email,
                     message=message)
    assert strategy.storage.friendshipRequest.objects.filter(
        from_user=from_user, to_user=to_user, message=message).count() > 0


def test_new_user_created(strategy, users, user_cls):
    email = 'newuser@ff.com'
    do_invite_friend(
        strategy, from_user=users[0], to_user_email=email, message='')
    do_invite_friend(
        strategy, from_user=users[1], to_user_email=email, message='')
    user = user_cls.objects.create(
        email=email, username='newuser', password='pw')
    new_user_created(strategy, user)
    assert not strategy.storage.friendInvitation.objects
    res = friendship_request_list(strategy, user)
    assert len(res['requesting']) == 0
    assert len(res['requested']) == 2


def test_load_friendship_request(strategy, users):
    from_user = users[0]
    to_user = users[1]
    token, request = do_invite_return_token_request(
        strategy, from_user, to_user)
    assert request.from_user == from_user
    assert request.to_user == to_user


def test_accept_friendship_request(strategy, users):
    from_user = users[0]
    to_user = users[1]
    token, request = do_invite_return_token_request(
        strategy, from_user, to_user)
    accept_friendship_request(strategy, token)
    assert not strategy.storage.friendshipRequest.objects.filter(pk=request.id)
    assert strategy.storage.friends.objects.filter(
        user1=from_user, user2=to_user).count() == 1


def test_reject_friendship_request(strategy, users):
    from_user = users[0]
    to_user = users[1]
    token, request = do_invite_return_token_request(
        strategy, from_user, to_user)
    reject_friendship_request(strategy, token)
    assert strategy.storage.friendshipRequest.objects.get(
        pk=request.id).rejected_at is not None


def test_cancel_friendship_request(strategy, users):
    from_user = users[0]
    to_user = users[1]
    token, request = do_invite_return_token_request(
        strategy, from_user, to_user)
    cancel_friendship_request(strategy, token)
    assert not strategy.storage.friendshipRequest.objects.filter(pk=request.id)


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


def test_friendship_request_list_rejected(strategy, users):
    user = users[0]

    # invite to user
    token, request = do_invite_return_token_request(
        strategy, users[1], user)
    reject_friendship_request(strategy, token)
    token, request = do_invite_return_token_request(
        strategy, users[2], user)
    accept_friendship_request(strategy, token)
    res = friendship_request_list_rejected(strategy, user)
    assert len(res['requesting']) == 0
    assert len(res['requested']) == 1

    # invite from user
    token, request = do_invite_return_token_request(
        strategy, user, users[3])
    reject_friendship_request(strategy, token)
    token, request = do_invite_return_token_request(
        strategy, user, users[4])
    accept_friendship_request(strategy, token)
    res = friendship_request_list_rejected(strategy, user)
    assert len(res['requesting']) == 1
    assert len(res['requested']) == 1


def test_friendlist(strategy, users):
    user = users[0]
    res = friendlist(strategy, user)
    assert not res
    token, request = do_invite_return_token_request(strategy, users[1], user)
    accept_friendship_request(strategy, token)
    token, request = do_invite_return_token_request(strategy, users[2], user)
    accept_friendship_request(strategy, token)
    token, request = do_invite_return_token_request(strategy, users[3], user)
    cancel_friendship_request(strategy, token)
    token, request = do_invite_return_token_request(strategy, users[4], user)
    reject_friendship_request(strategy, token)
    res = friendlist(strategy, user)
    assert len(res) == 2
