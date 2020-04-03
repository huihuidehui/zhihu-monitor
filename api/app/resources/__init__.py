#!/usr/bin/env python
# encoding: utf-8
from copy import deepcopy

from flask_restful import Resource, reqparse

from app.crawler.crawler_data import ZhSpider
from app.extensions.flask_httpauth import auth_token
from app.resources.setting import ModifyFramework, BaseSettings

from app.utils.requestdatabase import DatabaseRequest


class BaseResource(Resource):
    method_decorators = {'delete': [auth_token.login_required],
                         'post': [auth_token.login_required],
                         'put': [auth_token.login_required],
                         'get': [auth_token.login_required]
                         }  # 加入权限管理

    def options(self):
        return {'Allow': '*'}, 200, {'Access-Control-Allow-Origin': '*',
                                     'Access-Control-Allow-Methods': 'HEAD, OPTIONS, GET, POST, DELETE, PUT',
                                     'Access-Control-Allow-Headers': 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild',
                                     }

    def __init__(self):
        self.base_response_data = deepcopy(base_settings.base_response_data)
        # 接受的数据类型
        self.parser = reqparse.RequestParser()
        self.fields = None  # 过滤响应的字段
        # 请求数据库的对象
        self.requester = DatabaseRequest()

        # 爬虫对象
        self.crawler = ZhSpider()




ModifyFramework.apply()  # 应用对框架的修改
base_settings = BaseSettings()
from .question import Question, QuestionList
from .answer import Answer, AnswerList
from .login import Login
from .crawler import Crawler
