import sys
from itsdangerous import URLSafeSerializer


def import_module(name):
    __import__(name)
    return sys.modules[name]


def module_member(name):
    mod, member = name.rsplit('.', 1)
    module = import_module(mod)
    return getattr(module, member)


def get_strategy(strategy_cls, storage, *args, **kwargs):
    return strategy_cls(storage, *args, **kwargs)


def get_serializer(strategy):
    serializer = URLSafeSerializer(strategy.encryption_key())
    return serializer


def make_token(strategy, from_user, to_user):
    payload = {
        'from_user_id': "%s" % strategy.storage.user.get_id(from_user),
        'to_user_id': "%s" % strategy.storage.user.get_id(to_user)
    }
    return get_serializer(strategy).dumps(payload).encode('utf-8')
