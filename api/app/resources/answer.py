#!/usr/bin/env python
# encoding: utf-8
import datetime
from copy import deepcopy

from app.crawler.crawler_task import add_new_answer_crawler
from app.extensions import scheduler
from flask import current_app, g
from flask_restful import reqparse, marshal
from app.models import Answer as AnswerModel, VoteNum as VoteNumModel, CommentNum as CommentNumModel, Rank as RankModel
from app.resources import BaseResource, base_settings
from app.utils.util import get_values_by_keys, get_time_stamp
import re

class AnswerList(BaseResource):
    def __init__(self):
        super(AnswerList, self).__init__()

        # 接受的数据类型
        self.parser = reqparse.RequestParser()
        # get请求参数
        self.parser.add_argument('page', type=int, location='args')
        self.parser.add_argument('size', type=int, location='args')
        self.fields = deepcopy(base_settings.answers_fields)
        # 排序方式1：按时间升序排序，-1按时间降序；2按点赞增长升序排序，-2按点赞增长降序排序
        # 3按评论升序排序，-3按评论量降序排序,4按排名百分比排序,5按排名排序
        self.parser.add_argument('sortord', type=int, location='args')
        self.sort_methods = {
            1: AnswerModel.id,
            2: AnswerModel.current_vote_nums,
            3: AnswerModel.current_comment_nums,
            4: AnswerModel.current_rank
            # 2: AnswerModel.view_increment,
            # 3: AnswerModel.current_view_nums,
            # 4: AnswerModel.increase_percentage,
            # 5: AnswerModel.current_follower_nums
        }

    def get(self):
        response_data = deepcopy(self.base_response_data)
        page, size, sortord = get_values_by_keys(self.parser.parse_args(), [
            ('page', current_app.config['DEFAULTPAGE']),
            ('size', current_app.config['DEFAULTSIZE']),
            ('sortord', 1)
        ])
        response_data = self.make_pagination_data(page, size, sortord, response_data)
        return response_data, 200

    def make_pagination_data(self, page, size, sortord, data):
        """
        查询分页数据
        :param page:
        :param size:
        :param sortord:
        :param data:
        :return:
        """
        pagination_data = self.requester.get_anspagination_by_column(page, size, -sortord // abs(sortord),
                                                                     self.sort_methods[abs(sortord)], error_out=False)
        total_pages, answers, total_articles_num = pagination_data.pages, pagination_data.items, pagination_data.total  # 总页数和文章数据
        data['totalPage'] = total_pages
        data['currentPage'] = page
        data['totalNum'] = total_articles_num
        data['data'] = marshal(data=answers, fields=self.fields)  # 使用 marshal 格式化输出字段

        return data


class Answer(BaseResource):
    def __init__(self):
        super(Answer, self).__init__()
        self.parser.add_argument('answerZhiHuId', type=int)
        self.parser.add_argument('questionZhiHuId', type=int)
        self.parser.add_argument('answerUrl', type=str)
        self.parser.add_argument('startTime', type=int, default=0)  # 开始时间
        self.parser.add_argument('endTime', type=int, default=get_time_stamp())
        self.fields = base_settings.answer_fields

    def get(self):
        response_data = deepcopy(self.base_response_data)
        # answer_url = self.parser.parse_args().get('answerUrl')
        # try:
        # question_zhihuid, answer_zhihuid = re.findall(r".*question/(.*)/answer/(.*)", answer_url)[0]
        # question_zhihuid, answer_zhihuid = int(question_zhihuid), int(answer_zhihuid)
        answer_zhihuid = self.parser.parse_args().get('answerZhiHuId')
        question_zhihuid = self.parser.parse_args().get('questionZhiHuId')

        start_time = self.parser.parse_args().get('startTime')
        end_time = self.parser.parse_args().get('endTime')
        is_success, answer_data = self.requester.get_answer_by_zhihuid(answer_zhihuid=answer_zhihuid,
                                                                       question_zhihuid=question_zhihuid)
        if is_success:
            new_data = {
                # 回答者的昵称
                'title': answer_data.title,
                # 问题id不是数据库里的
                'questionZhiHuId': question_zhihuid,
                'questionTitle': answer_data.question_title,
                'voteNums': answer_data.vote_nums.filter(VoteNumModel.record_time >= start_time,
                                                         VoteNumModel.record_time <= end_time).all(),
                'commentNums': answer_data.comment_nums.filter(CommentNumModel.record_time >= start_time,
                                                               CommentNumModel.record_time <= end_time).all(),
                'rankNums': answer_data.ranks.filter(RankModel.record_time >= start_time,
                                                     RankModel.record_time <= end_time).all(),

            }

            response_data['data'] = marshal(new_data, fields=self.fields)
            return response_data
        else:
            response_data['res'] = 0
            response_data['message'] = 'error'
            return response_data

    def put(self):
        response_data = deepcopy(self.base_response_data)
        # answer_zhihuid = self.parser.parse_args().get('answerZhiHuId')
        # 问题id
        # question_zhihuid = self.parser.parse_args().get('questionZhiHuId')
        answer_url = self.parser.parse_args().get('answerUrl')
        question_zhihuid, answer_zhihuid = re.findall(r".*question/(.*)/answer/(.*)", answer_url)[0]
        question_zhihuid, answer_zhihuid = int(question_zhihuid), int(answer_zhihuid)
        is_success, question_data = self.requester.get_question_by_zhihuid(question_zhihuid)
        if is_success:
            # 数据库中的id
            question_id = question_data.id
            is_success = self.add_new_answer(answer_zhihuid=answer_zhihuid, question_zhihuid=question_zhihuid,
                                             question_id=question_id,
                                             question_title=question_data.title, user_id=g.user.id)
            # 回答在数据库的数据
            _, answer_data = self.requester.get_answer_by_zhihuid(answer_zhihuid, question_zhihuid)
            # answer_id为数据库的id
            answer_id = answer_data.id
            scheduler.add_job(func=add_new_answer_crawler, id="add_new_answer_crawler", trigger="date",
                              next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=5),
                              args=[question_zhihuid, answer_zhihuid, answer_id])
            return response_data, 200
        else:
            response_data['res'] = 0
            response_data['message'] = "error"
            return response_data

    def delete(self):
        response_data = deepcopy(self.base_response_data)
        answer_zhihuid = self.parser.parse_args().get('answerZhiHuId')
        question_zhihuid = self.parser.parse_args().get('questionZhiHuId')
        is_success, answer_data = self.requester.get_answer_by_zhihuid(answer_zhihuid=answer_zhihuid,
                                                                       question_zhihuid=question_zhihuid)
        if is_success:
            self.requester.delete(answer_data)
            self.requester.commit()
        else:
            response_data['res'] = 0
            response_data['message'] = "error"
        return response_data

    def add_new_answer(self, answer_zhihuid, question_zhihuid, question_id, question_title,user_id):
        """

        :param answer_zhihuid:
        :param question_zhihuid:
        :param question_model_id:
        :param question_title:
        :return:
        """
        try:
            new_answer = AnswerModel(answer_zhihuid=answer_zhihuid, question_zhihuid=question_zhihuid,
                                     question_id=question_id, question_title=question_title,user_id=user_id)
            self.requester.add(new_answer)
            self.requester.commit()
            return True
        except:
            return False
