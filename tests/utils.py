#!/usr/bin/env python
# -*- coding: utf-8 -*-
from friends.utils import make_token
from friends.actions import do_invite_friend, _load_friendship_request


def do_invite_return_token_request(strategy, from_user, to_user):
    do_invite_friend(strategy, from_user=from_user,
                     to_user_email=to_user.email, message="Hello!")
    token = make_token(strategy, from_user, to_user)
    request = _load_friendship_request(strategy, token)
    return token, request
