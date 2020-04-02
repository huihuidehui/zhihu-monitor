#!/usr/bin/env python
# encoding: utf-8
from copy import deepcopy

import flask_restful
from flask_restful import fields
from werkzeug.exceptions import HTTPException
from flask import abort as original_flask_abort


class BaseSettings(object):
    def __init__(self):
        # 过滤关注数的字段
        self.follower_nums_fields = {
            'value': fields.Integer(attribute='value'),
            # 'time': fields.DateTime(attribute='record_time'),
            'time': fields.Integer(attribute='record_time')
            # "articleNum": fields.Integer
        }
        # 过滤浏览数字段
        self.view_nums_fields = {
            'value': fields.Integer(attribute='value'),
            'time': fields.Integer(attribute='record_time')
        }
        # 过滤问题详情字段
        self.question_fields = {
            'questionTitle': fields.String(attribute='title'),
            'questionZhiHuId': fields.Integer(attribute='question_zhihuid'),
            'followerNums': fields.Nested(self.follower_nums_fields, attribute="followerNums"),
            'viewNums': fields.Nested(self.view_nums_fields, attribute="viewNums"),
            'currentFollowerNums': fields.Integer(attribute='current_follower_nums'),
            'currentViewNums': fields.Integer(attribute='current_view_nums')
        }
        # 过滤点赞
        self.vote_num_fields = {
            'value': fields.Integer(attribute='value'),
            'time': fields.Integer(attribute='record_time')
        }
        # 过滤排名
        self.rank_fields = {
            'value': fields.Integer(attribute='value'),
            'time': fields.Integer(attribute='record_time')
        }
        self.comment_fields = {
            'value': fields.Integer(attribute='value'),
            'time': fields.Integer(attribute='record_time')
        }
        # 过滤回答详情字段
        self.answer_fields = {
            'title': fields.String(attribute='title'),
            'questionZhiHuId': fields.Integer(attribute='questionZhiHuId'),
            'question': fields.String(attribute='questionTitle'),
            'voteNum': fields.Nested(self.vote_num_fields, attribute='voteNums'),
            'rank': fields.Nested(self.rank_fields, attribute='rankNums'),
            'commentNum': fields.Nested(self.comment_fields, attribute='commentNums')
        }
        self.answers_fields = {
            'title': fields.String(attribute='title'),
            'questionZhiHuId': fields.Integer(attribute='question_zhihuid'),
            'question': fields.String(attribute='question_title'),
            'voteNums': fields.Integer(attribute='current_vote_nums'),
            'rank': fields.Integer(attribute='current_rank'),
            'commentNums': fields.Integer(attribute='current_comment_nums'),
            'answerZhiHuId': fields.Integer(attribute='answer_zhihuid')
        }
        # 所有请求的默认响应
        self.base_response_data = {
            'res': 1,
            'message': 'successful',
        }

    def __repr__(self):
        return 'Api 共有的一些设置.'


# 对flask-restful的一些基本设置
class ModifyFramework(object):

    def __init__(self):
        pass

    @classmethod
    def abort(cls, http_status_code, **kwargs):
        """Raise a HTTPException for the given http_status_code. Attach any keyword
        arguments to the exception for later processing.
        用于覆盖原flask-restful中的abort，从而实现自定义参数验证错误信息。
        """
        try:
            original_flask_abort(http_status_code)
        except HTTPException as e:
            if len(kwargs):
                e.data = cls._make_parameter_error_response(http_status_code=e.code, data=kwargs)
            raise

    @classmethod
    def _make_parameter_error_response(cls, http_status_code, data):
        response_data = deepcopy(BaseSettings().base_response_data)
        response_data['message'] = response_data['message'] if data.get('message') is None else data.get('message')
        response_data['res'] = 0 if http_status_code == 400 else 1
        return response_data

    @classmethod
    def apply(cls):
        flask_restful.abort = ModifyFramework.abort  # 覆盖flask-restful原有的abort
