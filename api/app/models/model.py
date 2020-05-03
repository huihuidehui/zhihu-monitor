#!/usr/bin/env python
# encoding: utf-8

from flask import current_app, g

from app.extensions.flask_bcrypt import bcrypt
from app.extensions.flask_httpauth import auth_token, auth_basic
from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app.utils.util import get_time_stamp


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 问题id
    question_zhihuid = db.Column(db.Integer, unique=True)
    # 问题title
    title = db.Column(db.String(128))
    # 当前关注数
    current_follower_nums = db.Column(db.Integer)
    # 当前浏览数
    current_view_nums = db.Column(db.Integer)
    # 较上次增加浏览数
    view_increment = db.Column(db.Integer, default=0)
    # 增长比例
    increase_percentage = db.Column(db.Float, default=0.0)

    # 关注数
    follower_nums = db.relationship("FollowerNum", back_populates='question', lazy="dynamic")
    # 浏览数
    view_nums = db.relationship("ViewNum", back_populates='question', lazy="dynamic")
    # 需要监控的回答
    answers = db.relationship('Answer', back_populates='question', lazy="dynamic")
    # 总回答数
    answers_total = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # 所属用户
    # user = db.relationship('User', back_populates='questions')


class ViewNum(db.Model):
    # 多
    __tablename__ = "viewnum"
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.BigInteger, default=get_time_stamp())
    value = db.Column(db.BigInteger)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship("Question", back_populates="view_nums")

    @property
    def time_stamp(self):
        return int(self.record_time.timestamp())


class FollowerNum(db.Model):
    # 多
    __tablename__ = "followernum"
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.BigInteger, default=get_time_stamp())
    value = db.Column(db.BigInteger)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship("Question", back_populates="follower_nums")

    @property
    def time_stamp(self):
        return int(self.record_time.timestamp())


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_zhihuid = db.Column(db.BigInteger, unique=True)
    # 回答者的用户名
    title = db.Column(db.String(128))
    question_title = db.Column(db.String(128))
    # question_id
    current_vote_nums = db.Column(db.Integer)
    current_rank = db.Column(db.Integer)
    current_comment_nums = db.Column(db.Integer)
    question_zhihuid = db.Column(db.BigInteger)
    # 点赞数
    vote_nums = db.relationship("VoteNum", back_populates='answer', lazy="dynamic")
    # 评论数
    comment_nums = db.relationship("CommentNum", back_populates='answer', lazy="dynamic")
    # 排名
    ranks = db.relationship("Rank", back_populates="answer", lazy="dynamic")
    # 收藏
    collect_nums = db.relationship("CollectNums", back_populates="answer", lazy='dynamic')
    # 喜欢数
    like_nums = db.relationship("LikeNums", back_populates="answer", lazy='dynamic')

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', back_populates='answers')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def vote_nums_list(self):
        return self.vote_nums.all()

    @property
    def rank_nums_list(self):
        return self.ranks.all()

    @property
    def comment_nums_list(self):
        return self.comment_nums.all()


class LikeNums(db.Model):
    __tablename__ = "likenums"
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.BigInteger, default=get_time_stamp())
    value = db.Column(db.BigInteger)
    answer_id = db.Column(db.Integer, db.ForeignKey("answer.id"))
    answer = db.relationship("Answer", back_populates="like_nums")


class CollectNums(db.Model):
    __tablename__ = "collectnums"
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.BigInteger, default=get_time_stamp())
    value = db.Column(db.BigInteger)
    answer_id = db.Column(db.Integer, db.ForeignKey("answer.id"))
    answer = db.relationship("Answer", back_populates="collect_nums")


class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.BigInteger, default=get_time_stamp())
    value = db.Column(db.BigInteger)
    answer_id = db.Column(db.Integer, db.ForeignKey("answer.id"))
    answer = db.relationship("Answer", back_populates="ranks")

    @property
    def time_stamp(self):
        return int(self.record_time.timestamp())


class CommentNum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = "commentnum"
    record_time = db.Column(db.BigInteger, default=get_time_stamp())
    value = db.Column(db.BigInteger)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    answer = db.relationship("Answer", back_populates="comment_nums")

    @property
    def time_stamp(self):
        return int(self.record_time.timestamp())


class VoteNum(db.Model):
    __tablename__ = "votenum"
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.BigInteger, default=get_time_stamp())
    value = db.Column(db.BigInteger)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    answer = db.relationship("Answer", back_populates="vote_nums")

    @property
    def time_stamp(self):
        return int(self.record_time.timestamp())


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(128))
    questions = db.relationship('Question')
    answers = db.relationship('Answer')
    # questions = db.relationship("User", back_populates="question", lazy='dynamic')
    # questions = db.relationship('Question', back_populates='user', lazy="dynamic")
    # question = db.relationship('Question', back_populates='user_id')

    @staticmethod
    @auth_basic.verify_password
    def verify_password(username, password):
        """
        验证用户名和密码
        :param username:
        :param password:
        :return:
        """
        user = User.query.filter_by(name=username).first()
        if user is not None:
            if User.validate_password(user.password_hash, password):
                g.user = user
                return True
            else:
                False
        else:
            return False

    @staticmethod
    def set_password(password):
        """
        生成hash序列
        :param password:
        :return:
        """
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def validate_password(password_hash, password):
        """
        验证密码是否正确
        :param password_hash:
        :param password:
        :return:
        """
        return bcrypt.check_password_hash(password_hash, password)

    def generate_auth_token(self):
        """
        生成token
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['TOKEN_EXPIRATION_TIME'])
        return s.dumps({'id': self.id}).decode('utf-8')  # 返回值是一个二进制的

    @staticmethod
    @auth_token.verify_token
    def verify_auth_token(token):
        """
        验证token是否有效
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data['id'])
        g.user = user
        return True if user is not None else False
