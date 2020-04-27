#!/usr/bin/env python
# encoding: utf-8
from app.crawler.crawler_data import ZhSpider
from app.utils.requestdatabase import DatabaseRequest
from app.models import Question, ViewNum, FollowerNum, Answer, VoteNum, CommentNum, Rank
from app.utils.util import get_time_stamp

database_requester = DatabaseRequest()

zh_spider = ZhSpider()


def add_new_answer_crawler(question_zhihuid, answer_zhihuid, answer_id):
    """

    :param question_zhihuid:
    :param answer_zhihuid:
    :param answer_id:
    :return:
    """
    _, answer_data = database_requester.get_model_by_id(Answer, answer_id)
    vote_num, comment_num, rank, title = zh_spider.get_answer_data(answer_zhihuid, question_zhihuid)
    answer_data.title = title
    answer_data.current_vote_nums = vote_num
    answer_data.current_rank = rank
    answer_data.current_comment_nums = comment_num
    database_requester.commit()

    new_vote_num = VoteNum(value=vote_num, answer_id=answer_data.id, record_time=get_time_stamp())
    new_comment_num = CommentNum(value=comment_num, answer_id=answer_data.id, record_time=get_time_stamp())
    new_rank = Rank(value=rank, answer_id=answer_data.id, record_time=get_time_stamp())
    database_requester.add(new_vote_num)
    database_requester.add(new_comment_num)
    database_requester.add(new_rank)
    #
    database_requester.commit()


# @scheduler.task(trigger='interval', id='update_date', seconds=60)
def update_data():
    questions = database_requester.get_model_all(Question)
    print("更新问题")
    for question in questions:
        question_zhihuid = question.question_zhihuid
        follower_num, view_num, title = zh_spider.get_follower_view_title(question_zhihuid=question_zhihuid)
        # question.view_increment = view_num - question.current_follower_nums
        question.increase_percentage = (view_num - question.current_view_nums) / question.current_view_nums
        question.view_increment = view_num - question.current_view_nums
        question.current_follower_nums = follower_num
        question.current_view_nums = view_num

        new_view_num = ViewNum(value=view_num, question_id=question.id, record_time=get_time_stamp())
        new_follower_num = FollowerNum(value=follower_num, question_id=question.id, record_time=get_time_stamp())
        database_requester.add(new_view_num)
        database_requester.add(new_follower_num)
        database_requester.commit()
    print('问题更新完成')
    answers = database_requester.get_model_all(Answer)
    print("更新回答")
    for answer in answers:
        answer_zhihuid = answer.answer_zhihuid
        question_zhihuid = answer.question_zhihuid
        vote_num, comment_num, rank, title = zh_spider.get_answer_data(answer_zhihuid, question_zhihuid)
        new_vote_num = VoteNum(value=vote_num, answer_id=answer.id, record_time=get_time_stamp())
        new_comment_num = CommentNum(value=comment_num, answer_id=answer.id, record_time=get_time_stamp())
        new_rank = Rank(value=rank, answer_id=answer.id, record_time=get_time_stamp())
        database_requester.add(new_vote_num)
        database_requester.add(new_comment_num)
        database_requester.add(new_rank)
        database_requester.commit()

        answer.current_vote_nums = vote_num
        answer.current_rank = rank
        answer.current_comment_nums = comment_num
        answer.title = title
        database_requester.commit()

    print("回答更新完成")
# scheduler.add_job(update_data, "cron", hour=3)
