#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_create_friendship(strategy, users, app):
    url = '/request_friend'
    headers = {'Authenticate': 9999}

    with app.test_client() as c:
        resp = c.open(url, method='GET', headers=headers)
        assert resp.status_code == 405
        resp = c.open(url, method='POST', headers=headers, 
                      data=dict(email='new_user@ff.com'))
        assert resp.status_code == 401


