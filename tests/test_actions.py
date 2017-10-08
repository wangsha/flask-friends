# -*- coding: utf-8 -*-

import pytest
import mock

from utils import create_users
from friends.utils import get_strategy
from friends.actions import do_invite_friend
from friends.frameworks.flask.utils import get_helper
from flask import Blueprint, g, request, jsonify


@pytest.mark.xfail
def test_do_invite_friend(app, flask_mongoengine_storage):
    users = create_users(app, flask_mongoengine_storage)
    user_a = users[0]
    user_b = users[1]

    mock_strategy = mock.Mock()
    mock_strategy.storage = flask_mongoengine_storage
    do_invite_friend(mock_strategy, from_user=user_a.email,
                     to_user_email=user_b.email,
                     message="Hello! I'm Harry!")
