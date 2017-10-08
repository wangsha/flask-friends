# -*- coding: utf-8 -*-

"""

    conftest
    ~~~~~~~~

    Text fixtures
"""

import time
import pytest
import factory

from flask import Flask
from flask_mongoengine import MongoEngine
from friends.storagies.flask_mongoengine_storage import FlaskMongoengineStorage, init_friends
from friends.storagies.mongoengine_storage import MongoengineUserMixin, BaseMongoengineStorage


@pytest.fixture()
def flask_mongoengine_storage(app):
    db_name = 'flask_friends_test_%s' % str(time.time()).replace('.', '_')
    app.config['MONGODB_SETTINGS'] = {
        'db': db_name,
        'host': 'localhost',
        'port': 27017,
    }

    db = MongoEngine(app)

    class User(db.Document, MongoengineUserMixin):
        email = db.StringField(unique=True, max_length=255)
        username = db.StringField(max_length=255)
        password = db.StringField(max_length=255)
        active = db.BooleanField(default=True)

        meta = {'allow_inheritance': True}


    app.config['FRIENDS_USER_MODEL'] = User
    init_friends(app, db)
    yield FlaskMongoengineStorage()

    with app.app_context():
        db.connection.drop_database(db_name)


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.debug = True
    app.config['TESTING'] = True
    return app
