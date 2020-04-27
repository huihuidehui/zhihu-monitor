#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import func
from app.models import db, Question, Answer
from flask import g


class DatabaseRequest(object):
    def __init__(self):
        pass

    @staticmethod
    def get_answer_by_zhihuid(answer_zhihuid, question_zhihuid):
        """

        :param answer_zhihuid:
        :param question_zhihuid:
        :return:
        """
        data = Answer.query.filter_by(answer_zhihuid=answer_zhihuid).filter_by(
            question_zhihuid=question_zhihuid).first()
        return (False, None) if data is None else (True, data)

    @staticmethod
    def add(data):
        db.session.add(data)

    @staticmethod
    def commit():
        db.session.commit()

    # @staticmethod
    # def get_articles():
    #     return Article.query.all()
    #
    # @staticmethod
    # def get_new_posts(model, count):
    #     """
    #
    #     :param model:
    #     :param count:
    #     :return:
    #     """
    #     res = model.query.all()
    #     if len(res) > count:
    #         return res[:count]
    #     else:
    #         return res
    #
    # @staticmethod
    # def get_popular_posts(model, count):
    #     """
    #
    #     :param model:
    #     :param count:
    #     :return:
    #     """
    #     res = model.query.order_by(model.view_num).all()
    #     print(type(len(res)))
    # if len(res) > count:
    #     return res[-count:]
    # else:
    #     return res
    #
    @staticmethod
    def get_token():
        return g.user.generate_auth_token()

    #
    # def get_articles_by_tag_id(self, tag_id):
    #     """
    #
    #     :param tag_id:
    #     :return:
    #     """
    #     return Article.query.order_by(Article.post_time.desc()).filter_by(id=tag_id).all()
    #
    @staticmethod
    def get_model_all(model):
        """

        :param model:
        :return:
        """
        return model.query.all()

    @staticmethod
    def get_quepagination_by_increment(page, size, sortord, error_out):
        """
        按增长量查询
        :param page: 页码
        :param size: 每页的数据
        :param error_out: 不清楚
        :return:
        """
        if sortord == -1:
            # 升序
            data = Question.query.order_by(Question.view_increment).paginate(
                page=page,
                per_page=size,
                error_out=False)  # 从数据库中按时间顺序获取数据
        elif sortord == 1:
            # 降序
            data = Question.query.order_by(Question.view_increment.desc()).paginate(
                page=page,
                per_page=size,
                error_out=False
            )
        # self.pagination_data = data
        return data

    @staticmethod
    def get_quepagination_by_time(page, size, sortord, error_out=False):
        if sortord == 1:
            data = Question.query.order_by(Question.id.desc()).paginate(
                page=page,
                per_page=size,
                error_out=False)  # 从数据库中按时间顺序获取数据
        # self.pagination_data = data
        elif sortord == -1:
            data = Question.query.order_by(Question.id).paginate(
                page=page,
                per_page=size,
                error_out=False
            )
        return data

    @staticmethod
    def get_pagination(model, page, size, error_out):
        """

        :param page: 页码
        :param size: 每页的数据
        :param error_out: 不清楚
        :return:
        """
        data = model.query.paginate(
            page=page,
            per_page=size,
            error_out=False)  # 从数据库中按时间顺序获取数据
        # self.pagination_data = data
        return data

    #
    # @staticmethod
    # def get_tag_pagination(page, size, tag_id, error_out):
    #     """
    #
    #     :param tag_id:
    #     :param page: 页码
    #     :param size: 每页的数据
    #     :param error_out: 不清楚
    #     :return:
    #     """
    #     data = Tag.query.get(tag_id).articles.paginate(page=page, per_page=size, error_out=False)
    #     return data
    #
    # @staticmethod
    # def get_category_pagination(page, size, category_id, error_out):
    #     """
    #
    #     :param page:
    #     :param size:
    #     :param category_id:
    #     :param error_out:
    #     :return:
    #     """
    #     data = Category.query.get(category_id).articles.paginate(page=page, per_page=size, error_out=False)
    #     return data
    #
    # @staticmethod
    # def add(data):
    #     db.session.add(data)
    #
    # @staticmethod
    # def commit():
    #     db.session.commit()
    #
    @staticmethod
    def delete(data):
        db.session.delete(data)

    #
    @staticmethod
    def get_model_by_id(model, model_id):
        """
        使用model_id在model中查找数据. model_id不可为空
        :param model:
        :param model_id:
        :return:
        """
        data = model.query.get(model_id)
        return (False, None) if data is None else (True, data)

    #
    @staticmethod
    def get_question_by_zhihuid(question_zhihuid):
        """

        :param question_zhihuid:
        :return:
        """
        data = Question.query.filter_by(question_zhihuid=question_zhihuid).first()
        return (False, None) if data is None else (True, data)
