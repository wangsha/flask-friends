from friends.utils import make_token, get_serializer


def do_invite_friend(strategy, from_user, to_user_email, message):
    storage = strategy.storage
    if storage.user.user_exists(to_user_email):
        to_user = storage.user.get_user_by_email(to_user_email)
        storage.friendshipRequest.create(
            from_user=from_user, to_user=to_user, message=message
        )
        token = make_token(strategy, from_user, to_user)
        strategy.send_friendship_request_email(
            from_user=from_user,
            to_user=to_user,
            message=message,
            authentication_token=token,
        )
    else:
        storage.friendInvitation.create(
            from_user=from_user, to_user_email=to_user_email, message=message
        )
        strategy.send_friendship_invitation_email(
            from_user=from_user, to_user_email=to_user_email, message=message
        )


def new_user_created(strategy, user):
    """
    to be called by flask app
    :param strategy:
    :param user:
    :return:
    """
    storage = strategy.storage
    invitations = storage.friendInvitation.get_invitations_by_email(
        to_user_email=storage.user.get_email(user)
    )
    for invitation in invitations:
        storage.friendshipRequest.create(
            from_user=invitation.from_user, to_user=user, message=invitation.message
        )
        storage.friendInvitation.remove(invitation.id)


def _load_friendship_request(strategy, token):
    payload = get_serializer(strategy).loads(token)
    storage = strategy.storage
    from_user = storage.user.get_user_by_id(payload["from_user_id"])
    to_user = storage.user.get_user_by_id(payload["to_user_id"])
    request = storage.friendshipRequest.get_request(
        from_user=from_user, to_user=to_user
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
    res = list(
        storage.friendshipRequest.get_request_by_from_user(from_user=user)
    ) + list(storage.friendshipRequest.get_request_by_to_user(to_user=user))
    return res


def friendship_invitation_list(strategy, user):
    storage = strategy.storage
    res = storage.friendInvitation.get_invitations_by_from_user(from_user=user)
    return res


def friendship_request_list_rejected(strategy, user):
    storage = strategy.storage
    res = list(
        storage.friendshipRequest.get_rejected_request_by_from_user(from_user=user)
    ) + list(storage.friendshipRequest.get_rejected_request_by_to_user(to_user=user))
    return res


def friendlist(strategy, user):
    storage = strategy.storage
    res = storage.friends.get_friends(user=user)
    return res


def delete_friend(strategy, token):
    storage = strategy.storage
    payload = get_serializer(strategy).loads(token)
    storage = strategy.storage
    user1 = storage.user.get_user_by_id(payload["from_user_id"])
    user2 = storage.user.get_user_by_id(payload["to_user_id"])
    res = storage.friends.remove_friend(user1, user2)
    return res
