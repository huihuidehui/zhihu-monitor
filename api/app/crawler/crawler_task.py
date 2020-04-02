#!/usr/bin/env python
# encoding: utf-8
from app.crawler.crawler_data import ZhSpider
from app.utils.requestdatabase import DatabaseRequest
from app.models import Question, ViewNum, FollowerNum, Answer, VoteNum, CommentNum, Rank
from app.utils.util import get_time_stamp

database_requester = DatabaseRequest()

zh_spider = ZhSpider()


def add_new_answer_crawler(question_id, answer_name, answer_id):
    """

    :param question_id: 问题id
    :param answer_name:
    :param answer_id: 回答在数据库中的id
    :return:
    """
    vote_num, comment_num, rank = zh_spider.get_answer_data(answer_name, question_id)
    new_vote_num = VoteNum(value=vote_num, answer_id=answer_id, record_time=get_time_stamp())
    new_comment_num = CommentNum(value=comment_num, answer_id=answer_id, record_time=get_time_stamp())
    new_rank = Rank(value=rank, answer_id=answer_id, record_time=get_time_stamp())
    database_requester.add(new_vote_num)
    database_requester.add(new_comment_num)
    database_requester.add(new_rank)
    #
    database_requester.commit()
    # print(question_id)
    # print(answer_name)
    # print(answer_id)


# @scheduler.task(trigger='interval', id='update_date', seconds=60)
def update_data():
    questions = database_requester.get_model_all(Question)
    print("更新问题")
    for question in questions:
        question_id = question.question_id
        follower_num, view_num, title = zh_spider.get_follower_view_title(question_id=question_id)
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
        answer_name = answer.title
        question_id = answer.question_id
        vote_num, comment_num, rank = zh_spider.get_answer_data(answer_name, question_id)
        new_vote_num = VoteNum(value=vote_num, answer_id=answer.id, record_time=get_time_stamp())
        new_comment_num = CommentNum(value=comment_num, answer_id=answer.id, record_time=get_time_stamp())
        new_rank = Rank(value=rank, answer_id=answer.id, record_time=get_time_stamp())
        database_requester.add(new_vote_num)
        database_requester.add(new_comment_num)
        database_requester.add(new_rank)

        database_requester.commit()
    print("回答更新完成")
# scheduler.add_job(update_data, "cron", hour=3)
