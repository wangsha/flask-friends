from functools import wraps

from flask import current_app, g

from friends.utils import get_strategy, module_member

DEFAULTS = {
    "FRIENDS_STORAGE": "friends.storagies.FlaskMongoengineStorage",
    "FRIENDS_STRATEGY": "friends.strategy.BaseStrategy",
}


def get_helper(name, do_import=False):
    config = current_app.config.get(name, DEFAULTS.get(name, None))
    if do_import:
        config = module_member(config)
    return config


def load_strategy(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        g.strategy = get_strategy(
            current_app.extensions["friends"].strategy_cls,
            current_app.extensions["friends"].storage,
        )
        return func(*args, **kwargs)

    return wrapper
