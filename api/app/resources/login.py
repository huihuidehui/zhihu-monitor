#!/usr/bin/env python
# encoding: utf-8
from copy import deepcopy

from flask import g

from app.extensions.flask_httpauth import auth_basic
from . import BaseResource


class Login(BaseResource):
    method_decorators = {'get': [auth_basic.login_required]}

    def __init__(self):
        super(Login, self).__init__()

    def get(self):
        """
        登陆；登陆成功则返回token
        :return: token
        """
        response_data = deepcopy(self.base_response_data)
        response_data['token'] = self.requester.get_token()
        response_data['username'] = g.user.name
        return response_data, 200
