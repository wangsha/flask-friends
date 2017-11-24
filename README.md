# flask-friends

Inspired by [Python Social Auth](https://github.com/python-social-auth) and [Django Friendship](https://github.com/revsys/django-friendship)

This repository contains common code supporting friendship request, accept and reject feature and endpoints to retrieve a list of connected friends, rejected/open friendship request.

It's designed to be framework, storage database ignorant like `python-social-auth`. So far, `Flask` framework with `Mongoengine` storage has been implemented.
