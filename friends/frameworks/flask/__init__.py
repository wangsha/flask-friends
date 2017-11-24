from friends.storagies.flask_mongoengine_storage import (
    init_friends, FlaskMongoengineStorage,
)
from friends.utils import get_strategy
from friends.frameworks.flask.routes import friends_blueprint


class Friends(object):
    def __init__(self, app=None, **kwargs):
        self.app = app
        self.strategy_cls = None
        self.storage = None
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, db, user_cls, strategy_cls):
        init_friends(app, db, user_cls)
        self.storage = FlaskMongoengineStorage
        self.strategy_cls = strategy_cls
        app.extensions['friends'] = self

    def get_strategy(self):
        return get_strategy(self.strategy_cls, self.storage)
