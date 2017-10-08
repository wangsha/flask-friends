# -*- coding: utf-8 -*-


def create_users(app, flask_mongoengine_storage):
    User = flask_mongoengine_storage.user
    with app.app_context():
        users = [
            ('judy@ff.com', 'judy', None, True),
            ('harry@ff.com', 'harry', None, True),
            ('sha@ff.com', 'sha', None, True),
            ('walle@ff.com', 'walle', None, True),
            ('tony@ff.com', 'tony', None, False),
        ]
        for u in users:
            user = User(email=u[0], username=u[1], password=u[2],
                        active=u[3])
            user.save()
    return User.objects
