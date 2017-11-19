#!/usr/bin/env python
# -*- coding: utf-8 -*-
from friends.actions import _get_serializer


def make_token(strategy, from_user, to_user):
    payload = {
        'from_user_id': "%s" % from_user.get_id(),
        'to_user_id': "%s" % to_user.get_id()
    }
    return _get_serializer(strategy).dumps(payload).encode('utf-8')
