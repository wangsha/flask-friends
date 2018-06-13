from friends.utils import make_token, get_serializer


def do_invite_friend(strategy, from_user, to_user_email, message):
    if from_user.email == to_user_email:
        return False
    storage = strategy.storage
    if storage.user.user_exists(to_user_email):

        # check for existing friendship
        friendships = storage.friends.get_friends(from_user)
        for friendship in friendships:
            if friendship.user1.email == to_user_email or friendship.user2.email == to_user_email:
                return False
        to_user = storage.user.get_user_by_email(to_user_email)
        res = storage.friendshipRequest.create(
            from_user=from_user, to_user=to_user, message=message)
        if res:
            token = make_token(strategy, from_user, to_user)
            strategy.send_friendship_request_email(from_user=from_user, to_user=to_user,
                                                   message=message, authentication_token=token)
            return res
    else:
        res = storage.friendInvitation.create(from_user=from_user,
                                              to_user_email=to_user_email,
                                              message=message)
        if res:
            strategy.send_friendship_invitation_email(from_user=from_user,
                                                      to_user_email=to_user_email,
                                                      message=message)
        return res


def new_user_created(strategy, user):
    """
    to be called by flask app
    :param strategy:
    :param user:
    :return:
    """
    storage = strategy.storage
    invitations = storage.friendInvitation.get_invitations_by_email(
        to_user_email=storage.user.get_email(user))
    for invitation in invitations:
        storage.friendshipRequest.create(from_user=invitation.from_user,
                                         to_user=user,
                                         message=invitation.message)
        storage.friendInvitation.remove(invitation.id)


def _load_friendship_request(strategy, token):
    payload = get_serializer(strategy).loads(token)
    storage = strategy.storage
    from_user = storage.user.get_user_by_id(payload['from_user_id'])
    to_user = storage.user.get_user_by_id(payload['to_user_id'])
    request = storage.friendshipRequest.get_request(
        from_user=from_user,
        to_user=to_user
    )
    return request


def accept_friendship_request(strategy, token):
    request = _load_friendship_request(strategy, token)
    storage = strategy.storage
    storage.friendshipRequest.remove(request.id)
    storage.friends.create(user1=request.from_user, user2=request.to_user)


def reject_friendship_request(strategy, token):
    request = _load_friendship_request(strategy, token)
    strategy.storage.friendshipRequest.reject(request.id)


def cancel_friendship_request(strategy, token):
    request = _load_friendship_request(strategy, token)
    strategy.storage.friendshipRequest.remove(request.id)


def friendship_request_list(strategy, user):
    storage = strategy.storage
    res = list(storage.friendshipRequest.get_request_by_from_user(from_user=user))
    res += list(storage.friendshipRequest.get_request_by_to_user(to_user=user))
    return res


def friendship_invitation_list(strategy, user):
    storage = strategy.storage
    res = storage.friendInvitation.get_invitations_by_from_user(from_user=user)
    return res


def friendship_request_list_rejected(strategy, user):
    storage = strategy.storage
    res = list(storage.friendshipRequest.get_rejected_request_by_from_user(from_user=user))
    res += list(storage.friendshipRequest.get_rejected_request_by_to_user(to_user=user))
    return res


def friendlist(strategy, user):
    storage = strategy.storage
    res = storage.friends.get_friends(user=user)
    return res


def delete_friend(strategy, token):
    storage = strategy.storage
    payload = get_serializer(strategy).loads(token)
    storage = strategy.storage
    user1 = storage.user.get_user_by_id(payload['from_user_id'])
    user2 = storage.user.get_user_by_id(payload['to_user_id'])
    res = storage.friends.remove_friend(
        user1,
        user2
    )
    return res
