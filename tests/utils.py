#!/usr/bin/env python
# -*- coding: utf-8 -*-
from friends.actions import _get_serializer


def make_token(strategy, from_user, to_user):
    # TODO(@Judy): 
    payload = {
        'from_user_id': "%s" % strategy.storage.user.get_id(from_user),
        'to_user_id': "%s" % strategy.storage.user.get_id(to_user)
    }
    return _get_serializer(strategy).dumps(payload).encode('utf-8')
