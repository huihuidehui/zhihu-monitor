#!/usr/bin/env python
# encoding: utf-8
import datetime
from copy import deepcopy
from app.crawler.crawler_task import update_data
from app.extensions import scheduler
from flask_restful import reqparse
from app.resources import BaseResource


class Crawler(BaseResource):
    def __init__(self):
        super(Crawler, self).__init__()

        # 接受的数据类型
        self.parser = reqparse.RequestParser()
        # get请求参数
        # self.parser.add_argument('page', type=int, location='args')
        # self.parser.add_argument('size', type=int, location='args')
        # self.fields = deepcopy(base_settings.answers_fields)

    def get(self):
        response_data = deepcopy(self.base_response_data)
        scheduler.add_job(func=update_data, id="start_crawler", trigger="date",
                          next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=5))

        return response_data, 200
