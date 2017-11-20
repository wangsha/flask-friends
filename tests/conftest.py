# -*- coding: utf-8 -*-

"""

    conftest
    ~~~~~~~~

    Text fixtures
"""

import time
import mock
import pytest

from flask import Flask
from flask_mongoengine import MongoEngine

from mongoengine.connection import disconnect
from friends.strategy import BaseStrategy
from friends.storagies.flask_mongoengine_storage import FlaskMongoengineStorage, init_friends
from friends.storagies.mongoengine_storage import MongoengineUserMixin


@pytest.fixture()
def flask_mongoengine_storage(app):
    db_name = 'flask_friends_test_%s' % str(time.time()).replace('.', '_')
    app.config['MONGODB_SETTINGS'] = {
        'db': db_name,
        'host': 'localhost',
        'port': 27018,
    }
    db = MongoEngine(app)

    class User(db.Document, MongoengineUserMixin):
        email = db.StringField(unique=True, max_length=255)
        username = db.StringField(max_length=255)
        password = db.StringField(max_length=255)
        active = db.BooleanField(default=True)

        USERNAME_FIELD = 'email'
        meta = {'allow_inheritance': True}

    app.config['FRIENDS_USER_MODEL'] = User
    init_friends(app, db)
    yield FlaskMongoengineStorage()

    with app.app_context():
        db.connection.drop_database(db_name)
        # Mongoengine keep a global state of the connections that must be
        # reset before each test.
        # Given it doesn't expose any method to get the list of registered
        # connections, we have to do the cleaning by hand...
        disconnect()


@pytest.fixture()
def users(app, flask_mongoengine_storage):
    User = flask_mongoengine_storage.user
    with app.app_context():
        users = [
            ('judy@ff.com', 'judy', None, True),
            ('harry@ff.com', 'harry', None, True),
            ('sha@ff.com', 'sha', None, True),
            ('walle@ff.com', 'walle', None, True),
            ('tony@ff.com', 'tony', None, False),
            ('bob@ff.com', 'bob', None, False),
        ]
        for u in users:
            user = User(email=u[0], username=u[1], password=u[2],
                        active=u[3])
            user.save()
    users = User.objects
    yield users
    for u in users:
        u.delete()


@pytest.fixture()
def strategy(flask_mongoengine_storage):
    class TestStrategy(BaseStrategy):

        def authenticate_request(self, authorization):
            pass

        def encryption_key(self):
            return 'IamSoSecret!!'

        def send_friendship_invitation_email(self, from_user, to_user_email, message):
            pass

        def send_friendship_request_email(self, from_user, to_user, message, authentication_token):
            pass

    strategy = TestStrategy(storage=flask_mongoengine_storage)
    return strategy


@pytest.fixture()
def app():
    _app = Flask(__name__)
    _app.debug = True
    _app.config['TESTING'] = True
    return _app
