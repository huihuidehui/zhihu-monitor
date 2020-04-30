#!/usr/bin/env python
# encoding: utf-8

from copy import deepcopy
from flask import current_app
from flask_restful import reqparse, marshal
from app.models import Question as QuestionModel, FollowerNum, ViewNum
from app.resources import BaseResource, base_settings
from app.utils.util import get_values_by_keys, get_time_stamp


class QuestionList(BaseResource):
    def __init__(self):
        super(QuestionList, self).__init__()

        # 接受的数据类型
        self.parser = reqparse.RequestParser()
        # get请求参数
        self.parser.add_argument('page', type=int, location='args')
        self.parser.add_argument('size', type=int, location='args')
        # 排序方式1：按时间升序排序，-1按时间降序；2按浏览量增长升序排序，-2按浏览量增长降序排序
        # 3按浏览量升序排序，-3按浏览量降序排序,4按浏览量增加百分比排序,5按关注数排序
        self.parser.add_argument('sortord', type=int, location='args')
        # self.parser.add_argument('')
        # 用于问题文章响应
        self.fields = deepcopy(base_settings.question_fields)
        self.fields.pop('followerNums')
        self.fields.pop('viewNums')

        self.sort_methods = {
            1: QuestionModel.id,
            2: QuestionModel.view_increment,
            3: QuestionModel.current_view_nums,
            4: QuestionModel.increase_percentage,
            5: QuestionModel.current_follower_nums
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
        查询分页数据.
        :param page: 页数
        :param size: 每页的个数
        :param data: 返回的数据
        :return: data
        """
        pagination_data = self.requester.get_quepagination_by_column(page, size, -sortord // (abs(sortord)),
                                                                     self.sort_methods[abs(sortord)], error_out=False)
        total_pages, questions, total_articles_num = pagination_data.pages, pagination_data.items, pagination_data.total  # 总页数和文章数据
        data['totalPage'] = total_pages
        data['currentPage'] = page
        data['totalNum'] = total_articles_num
        data['data'] = marshal(data=questions, fields=self.fields)  # 使用 marshal 格式化输出字段

        return data


class Question(BaseResource):

    # def get(self):
    def __init__(self):
        super(Question, self).__init__()
        # 请求添加问题的id
        self.parser.add_argument('questionZhiHuId', type=int)
        self.parser.add_argument('startTime', type=int, default=0)  # 开始时间
        self.parser.add_argument('endTime', type=int, default=get_time_stamp())  # 截至时间
        self.fields = base_settings.question_fields

    def get(self):
        response_data = {'res': 1, 'data': None}
        # 根据id请求数据库中的问题详情。
        question_zhihuid = self.parser.parse_args().get('questionZhiHuId')
        start_time = self.parser.parse_args().get('startTime')
        end_time = self.parser.parse_args().get('endTime')

        is_success, question_data = self.requester.get_question_by_zhihuid(question_zhihuid)

        new_data = {
            'question_zhihuid': question_data.question_zhihuid,
            'title': question_data.title,
            'followerNums': question_data.follower_nums.filter(FollowerNum.record_time >= start_time,
                                                               FollowerNum.record_time <= end_time).all(),
            'viewNums': question_data.view_nums.filter(ViewNum.record_time >= start_time,
                                                       ViewNum.record_time <= end_time).all(),
            'current_follower_nums': question_data.current_follower_nums,
            'current_view_nums': question_data.current_view_nums,
            'view_increment': question_data.view_increment,
            'increase_percentage': question_data.increase_percentage
            # 'viewIncrement': fields.Integer(attribute="view_increment"),
            # 'increasePercentage': fields.Float(attribute="increase_percentage")
        }

        if is_success:
            response_data['data'] = marshal(new_data, fields=self.fields)
        return response_data
        # return [endtime,starttime]

    def put(self):
        response_data = deepcopy(self.base_response_data)
        question_zhihuid = self.parser.parse_args().get("questionZhiHuId")
        # 获取当前时间该的问题关注数和浏览数和标题
        follower_nums, view_nums, title = self.crawler.get_follower_view_title(question_zhihuid)

        # 根据问题id提交到数据库
        new_question = self.build_new_question(question_zhihuid, title, follower_nums, view_nums)
        # 提交到数据库
        try:
            self.requester.add(new_question)
            self.requester.commit()

            new_follower_num = FollowerNum(question_id=new_question.id, value=follower_nums,
                                           record_time=get_time_stamp())
            new_view_num = ViewNum(question_id=new_question.id, value=view_nums, record_time=get_time_stamp())
            self.requester.add(new_follower_num)
            self.requester.add(new_view_num)

            # 提交
            self.requester.commit()

            return response_data
        except:
            response_data['res'] = 0
            response_data['message'] = "error"
            return response_data

    def delete(self):
        response_data = deepcopy(self.base_response_data)
        question_zhihuid = self.parser.parse_args().get('questionZhiHuId')
        res, data = self.requester.get_question_by_zhihuid(question_zhihuid)
        if res:
            self.requester.delete(data)
            self.requester.commit()
            response_data['res'] = 1
        else:
            response_data['res'] = 0
            response_data['message'] = "error"
        return response_data, 200

    def build_new_question(self, question_zhihuid, title, follower_nums, view_nums):
        """

        :param question_zhihuid:
        :param title:
        :param follower_nums:
        :param view_nums:
        :return:
        """
        new_question = QuestionModel(question_zhihuid=question_zhihuid, title=title,
                                     current_follower_nums=follower_nums,
                                     current_view_nums=view_nums)
        return new_question
