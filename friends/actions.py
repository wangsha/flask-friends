def do_invite_friend(strategy, from_user, to_user_email, message):
    storage = strategy.storage
    if storage.user.user_exists(to_user_email):
        to_user = storage.user.get_user_by_email(to_user_email)
        storage.friendshipRequest.create(from_user=from_user, to_user=to_user, message=message)
        strategy.send_friendship_request_email(from_user=from_user, to_user=to_user,
                                               message=message)
    else:
        storage.friendshipInvitation.create(from_user=from_user, to_user_email=to_user_email,
                                            message=message)
        strategy.send_friendship_invitation_email(from_user=from_user,
                                                  to_user_email=to_user_email, message=message)


def new_user_created(strategy, user):
    storage = strategy.storage
    invitations = storage.friendshipInvitation.get_invitations_by_email(
        to_user_email=storage.friendshipInvitation.get_email(user))
    for invitation in invitations:
        storage.friendshipRequest.create(from_user=invitation.from_user,
                                         to_user=user,
                                         message=invitation.message)
        storage.friendshipInvitation.remove(invitation.id)


def accept_friendship_request(strategy, from_user, to_user):
    storage = strategy.storage
    request = storage.friendshipRequest.get_request(
        from_user=from_user,
        to_user=to_user
    )

    storage.friendshipRequest.remove(request.id)

    storage.friends.create(user1=from_user, user2=to_user)


def reject_friendship_request(strategy, from_user, to_user):
    storage = strategy.storage
    request = storage.friendshipRequest.get_request(
        from_user=from_user,
        to_user=to_user
    )


    storage.friendshipRequest.reject(request.id)


def cancel_friendship_request(strategy, from_user, to_user):
    storage = strategy.storage
    request = storage.friendshipRequest.get_request(
        from_user=from_user,
        to_user=to_user
    )

    storage.friendshipRequest.remove(request.id)


def friendship_request_list(strategy, user):
    storage = strategy.storage
    res = {
        'requesting': storage.friendshipRequest.get_request_by_from_user(from_user=user),
        'requested': storage.friendshipRequest.get_request_by_to_user(to_user=user)
    }
    return res


def friendship_request_list_rejected(strategy, user):
    storage = strategy.storage
    res = {
        'requesting': storage.friendshipRequest.get_rejected_request_by_from_user(from_user=user),
        'requested': storage.friendshipRequest.get_rejected_request_by_to_user(to_user=user)
    }
    return res


def friendlist(strategy, user):
    storage = strategy.storage
    res = storage.friends.get_friends(user=user)
    return res
