#!/usr/bin/env python
# encoding: utf-8
import datetime
from copy import deepcopy

from app.crawler.crawler_task import add_new_answer_crawler
from app.extensions import scheduler
from flask import current_app
from flask_restful import reqparse, marshal
from app.models import Answer as AnswerModel, VoteNum as VoteNumModel, CommentNum as CommentNumModel, Rank as RankModel
from app.resources import BaseResource, base_settings
from app.utils.util import get_values_by_keys, get_time_stamp


class AnswerList(BaseResource):
    def __init__(self):
        super(AnswerList, self).__init__()

        # 接受的数据类型
        self.parser = reqparse.RequestParser()
        # get请求参数
        self.parser.add_argument('page', type=int, location='args')
        self.parser.add_argument('size', type=int, location='args')
        self.fields = deepcopy(base_settings.answers_fields)

    def get(self):
        response_data = deepcopy(self.base_response_data)
        page, size = get_values_by_keys(self.parser.parse_args(), [
            ('page', current_app.config['DEFAULTPAGE']),
            ('size', current_app.config['DEFAULTSIZE'])
        ])
        response_data = self.make_pagination_data(page, size, response_data)
        return response_data, 200

    def make_pagination_data(self, page, size, data):
        """
        查询分页数据.
        :param page: 页数
        :param size: 每页的个数
        :param data: 返回的数据
        :return: data
        """
        pagination_data = self.requester.get_pagination(AnswerModel, page, size, error_out=False)
        total_pages, answers, total_articles_num = pagination_data.pages, pagination_data.items, pagination_data.total  # 总页数和文章数据
        data['totalPage'] = total_pages
        data['currentPage'] = page
        data['totalNum'] = total_articles_num
        data['data'] = marshal(data=answers, fields=self.fields)  # 使用 marshal 格式化输出字段

        return data


class Answer(BaseResource):
    def __init__(self):
        super(Answer, self).__init__()
        self.parser.add_argument('answerName', type=str)
        self.parser.add_argument('questionId', type=int)
        self.parser.add_argument('startTime', type=int, default=0)  # 开始时间
        self.parser.add_argument('endTime', type=int, default=get_time_stamp())
        self.fields = base_settings.answer_fields

    def get(self):
        response_data = deepcopy(self.base_response_data)
        answer_name = self.parser.parse_args().get('answerName')
        question_id = self.parser.parse_args().get('questionId')

        start_time = self.parser.parse_args().get('startTime')
        end_time = self.parser.parse_args().get('endTime')
        is_success, answer_data = self.requester.get_answer_by_name(answer_name=answer_name, question_id=question_id)
        if is_success:
            new_data = {
                'title': answer_data.title,
                'questionId': question_id,
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
        answer_name = self.parser.parse_args().get('answerName')
        question_id = self.parser.parse_args().get('questionId')
        is_success, question_data = self.requester.get_question_by_id(question_id)
        is_success = self.add_new_answer(answer_name=answer_name, question_id=question_id,
                                         question_title=question_data.title)
        if is_success:
            # 回答在数据库的数据
            _, answer_data = self.requester.get_answer_by_name(answer_name, question_id)
            scheduler.add_job(func=add_new_answer_crawler, id="add_new_answer_crawler", trigger="date",
                              next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=5),
                              args=[question_id, answer_name, answer_data.id])
            return response_data, 200
        else:
            response_data['res'] = 0
            response_data['message'] = "error"
            return response_data

    def delete(self):
        response_data = deepcopy(self.base_response_data)
        answer_name = self.parser.parse_args().get('answerName')
        question_id = self.parser.parse_args().get('questionId')
        is_success, answer_data = self.requester.get_answer_by_name(answer_name=answer_name, question_id=question_id)
        if is_success:
            self.requester.delete(answer_data)
            self.requester.commit()
        else:
            response_data['res'] = 0
            response_data['message'] = "error"
        return response_data

    def add_new_answer(self, answer_name, question_id, question_title):
        """
        增加新的回答
        :param answer_name:
        :param question_id:
        :return: bool
        """
        try:
            new_answer = AnswerModel(title=answer_name, question_id=question_id, question_title=question_title)
            self.requester.add(new_answer)
            self.requester.commit()
            return True
        except:
            return False
