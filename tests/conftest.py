# -*- coding: utf-8 -*-

"""

    conftest
    ~~~~~~~~

    Text fixtures
"""

import pytest

from flask import Flask
from flask_mongoengine import MongoEngine
from friends.storagies.flask_mongoengine_storage import init_friends


@pytest.fixture()
def db():
    return MongoEngine()


@pytest.fixture()
def friend_user_model(db):

    class User(db.Document):
        email = db.StringField(unique=True, max_length=255)
        username = db.StringField(max_length=255)
        password = db.StringField(max_length=255)
        active = db.BooleanField(default=True)


@pytest.fixture()
def app(friend_user_model, db):
    app = Flask(__name__)
    app.debug = True
    app.config['TESTING'] = True
    app.config['FRIENDS_USER_MODEL'] = friend_user_model
    app.init_app(app)
    init_friends(app, db)
