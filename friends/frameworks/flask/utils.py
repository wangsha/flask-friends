from functools import wraps

from flask import current_app, g

from friends.utils import get_strategy, module_member

DEFAULTS = {
    'FRIENDS_STORAGE': 'social_flask_sqlalchemy.models.FlaskStorage',
    'FRIENDS_STRATEGY': 'social_flask.strategy.FlaskStrategy'
}


def get_helper(name, do_import=False):
    config = current_app.config.get(name,
                                    DEFAULTS.get(name, None))
    if do_import:
        config = module_member(config)
    return config


def load_strategy():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            g.strategy = get_strategy(get_helper('FRIENDS_STRATEGY'),
                                      get_helper('FRIENDS_STORAGE'))
            return func(*args, **kwargs)

        return wrapper

    return decorator
