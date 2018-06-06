# -*- coding: utf-8 -*-
from mock import Mock

from friends.utils import make_token
from friends.actions import do_invite_friend, friendship_request_list,\
    accept_friendship_request, new_user_created, reject_friendship_request,\
    cancel_friendship_request, friendlist, friendship_request_list_rejected,\
    delete_friend, friendship_invitation_list


def test_do_invite_friend(app, users, friends):
    strategy = friends.get_strategy()
    from_user = users[0]
    message = 'Hello!'

    # to_user does not exists
    to_user_email = 'idontexist@ff.com'
    mock_invitation_email = Mock()
    strategy.send_friendship_invitation_email = mock_invitation_email
    do_invite_friend(strategy, from_user=from_user,
                     to_user_email=to_user_email,
                     message=message)
    assert mock_invitation_email.call_count == 1
    assert strategy.storage.friendInvitation.objects.filter(
        from_user=from_user, to_user_email=to_user_email, message="Hello!"
    ).count() > 0

    # to self
    to_user = from_user
    mock_request_email = Mock()
    strategy.send_friendship_request_email = mock_request_email
    do_invite_friend(strategy, from_user=from_user,
                     to_user_email=to_user.email,
                     message=message)
    assert mock_request_email.call_count == 0
    assert strategy.storage.friendshipRequest.objects.filter(
        from_user=from_user, to_user=to_user, message=message).count() == 0

    # to_user exists
    to_user = users[1]
    mock_request_email = Mock()
    strategy.send_friendship_request_email = mock_request_email
    do_invite_friend(strategy, from_user=from_user,
                     to_user_email=to_user.email,
                     message=message)
    assert mock_request_email.call_count == 1
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
    assert len(res) == 2


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

    # already friends
    from_user = users[1]
    to_user = users[2]
    strategy.storage.friends.create(user1=from_user, user2=to_user)
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
    assert len(res) == 2

    # 1 invite from user_a to user_b
    do_invite_friend(
        strategy, from_user=user_a, to_user_email=user_b.email, message='')
    res = friendship_request_list(strategy, user_a)
    assert len(res) == 3
    res = friendship_request_list(strategy, user_b)
    assert len(res) == 1


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
    assert len(res) == 1

    # invite from user
    token, request = do_invite_return_token_request(
        strategy, user, users[3])
    reject_friendship_request(strategy, token)
    token, request = do_invite_return_token_request(
        strategy, user, users[4])
    accept_friendship_request(strategy, token)
    res = friendship_request_list_rejected(strategy, user)
    assert len(res) == 2


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


def test_delete_friend(strategy, users):
    from_user = users[0]
    strategy.storage.friends.create(from_user, user2=users[1])
    strategy.storage.friends.create(from_user, user2=users[2])

    token = make_token(strategy, from_user, users[1])
    delete_friend(strategy, token)
    res = friendlist(strategy, user=from_user)
    assert len(res) == 1

    token = make_token(strategy, from_user, users[2])
    delete_friend(strategy, token)
    res = friendlist(strategy, user=from_user)
    assert len(res) == 0


def test_friendship_invitation_list(strategy, users):
    from_user = users[0]
    res = friendship_invitation_list(strategy, from_user)
    assert len(res) == 0
    do_invite_friend(strategy, from_user, users[1].email, 'Hi!')
    do_invite_friend(strategy, from_user, 'aa@ff.com', 'Hi!')
    res = friendship_invitation_list(strategy, from_user)
    assert len(res) == 1
    do_invite_friend(strategy, from_user, 'aa@ff.com', 'Hi!')
    res = friendship_invitation_list(strategy, from_user)
    assert len(res) == 1
    do_invite_friend(strategy, from_user, 'bb@ff.com', 'Hi!')
    res = friendship_invitation_list(strategy, from_user)
    assert len(res) == 2
