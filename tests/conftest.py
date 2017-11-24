# -*- coding: utf-8 -*-

"""

    conftest
    ~~~~~~~~

    Text fixtures
"""

import time
import pytest

from flask import Flask
from flask_mongoengine import MongoEngine

from mongoengine.connection import disconnect

from friends.frameworks.flask.routes import friends_blueprint
from friends.strategy import BaseStrategy
from friends.frameworks.flask import Friends


@pytest.fixture()
def db(app):
    db_name = 'flask_friends_test_%s' % str(time.time()).replace('.', '_')
    app.config['MONGODB_SETTINGS'] = {
        'db': db_name,
        'host': 'localhost',
        'port': 27017,
    }
    _db = MongoEngine(app)

    yield _db

    with app.app_context():
        _db.connection.drop_database(db_name)
        # Mongoengine keep a global state of the connections that must be
        # reset before each test.
        # Given it doesn't expose any method to get the list of registered
        # connections, we have to do the cleaning by hand...
        disconnect()


@pytest.fixture
def user_cls(db):
    class User(db.Document):
        email = db.StringField(unique=True, max_length=255)
        username = db.StringField(max_length=255)
        password = db.StringField(max_length=255)
        active = db.BooleanField(default=True)

        USERNAME_FIELD = 'email'
        meta = {'allow_inheritance': True}
    yield User


@pytest.fixture()
def users(app, user_cls):
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
            user = user_cls(email=u[0], username=u[1], password=u[2],
                            active=u[3])
            user.save()
    return user_cls.objects


@pytest.fixture()
def strategy_cls(app, db):
    class TestStrategy(BaseStrategy):

        def authenticate_request(self, authorization):
            if not authorization:
                return None
            user = self.storage.user.get_user_by_id(authorization)
            return user

        def encryption_key(self):
            return 'IamSoSecret!!'

        def send_friendship_invitation_email(self, from_user, to_user_email, message):
            pass

        def send_friendship_request_email(self, from_user, to_user, message, authentication_token):
            pass

    return TestStrategy


@pytest.fixture
def friends(app, db, user_cls, strategy_cls):
    friends = Friends(
        app, db=db, user_cls=user_cls, strategy_cls=strategy_cls)
    return friends


@pytest.fixture
def strategy(friends):
    return friends.get_strategy()


@pytest.fixture()
def app():
    _app = Flask(__name__)
    _app.debug = True
    _app.config['TESTING'] = True
    _app.register_blueprint(friends_blueprint)
    with _app.app_context():
        yield _app
