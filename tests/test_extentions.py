from friends.frameworks.flask import Friends


def test_friends_init(app, db, user_cls, strategy_cls):
    friends = Friends()
    assert friends.app is None

    friends = Friends(app, db=db, user_cls=user_cls, strategy_cls=strategy_cls)
    assert friends.app == app
