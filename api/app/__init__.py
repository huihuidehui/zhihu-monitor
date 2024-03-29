#!/usr/bin/env python
# encoding: utf-8
import datetime
import time

import click
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from app.extensions import scheduler
from app.extensions.flask_bcrypt import bcrypt
from app.models import db, Question as QuestionModel, Answer as AnswerModel, User as UserModel
from app.resources import Question, Login, QuestionList, Answer, AnswerList, Crawler
from flask_cors import CORS
from app.crawler.crawler_task import update_data
import requests


def create_app():
    app = Flask(__name__)
    # 加载配置文件
    # app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')

    # @app.route("/home")
    # def hello():
    #     return "hello world"
    # 初始化数据库
    init_database(app)

    # 注册api
    register_api(app)

    # 注册命令
    register_commands(app)
    # 注册插件
    register_extensions(app)
    # 解决跨域请求问题
    CORS(app)

    # 创建爬虫任务
    create_crawler_task(app)

    # 数据库迁移插件
    create_migrate(app)

    return app


def create_migrate(app):
    migrate = Migrate(app, db)




def create_crawler_task(app):
    # 定时抓取数据
    scheduler.add_job(func=update_data, id="update_data", trigger="cron", hour=app.config['HOUR'],
                      minute=app.config['MINUTE'])
    # 每隔12小时爬一次
    # scheduler.add_job(func=update_data, trigger='interval', id='update_date', seconds=43200)
    # scheduler.add_job(func=test, trigger='interval', id='test', seconds=10)

    # scheduler.add_job(func=test, id="test", trigger="date",
    #                   next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=5))



def register_extensions(app):
    bcrypt.init_app(app)
    scheduler.init_app(app)


def init_database(app):
    db.init_app(app)
    db.create_all(app=app)
    db.app = app


def register_api(app):
    api = Api(app)
    api.add_resource(Question, "/question")
    api.add_resource(Login, "/login")
    api.add_resource(QuestionList, "/questions")
    api.add_resource(Answer, "/answer")
    api.add_resource(AnswerList, "/answers")
    api.add_resource(Crawler, "/crawler")


def register_commands(app):
    @app.cli.command(help='Reset database.')
    def resetdatabase():  # 重置数据库
        db.drop_all(app=app)
        db.create_all(app=app)
        click.echo('Reset database, successful.')

    @app.cli.command(help="add new user")
    @click.option('-u', prompt=True, help='username')
    @click.option('-p', prompt=True, hide_input=True, confirmation_prompt=True, help='password')
    def adduser(u, p):
        new_user = UserModel(name=u, password_hash=UserModel.set_password(p))
        db.session.add(new_user)
        db.session.commit()
        click.echo("Successful!")

    @app.cli.command(help='''Initialize the blog Use \'--help\' for more information.''')
    @click.option('-u', prompt=True, help='username')
    @click.option('-p', prompt=True, hide_input=True, confirmation_prompt=True, help='password')
    def init(u, p):
        # 初始化数据库
        db.init_app(app)
        db.create_all(app=app)
        # 新建用户
        new_user = UserModel(name=u, password_hash=UserModel.set_password(p))
        db.session.add(new_user)
        db.session.commit()

        click.echo('Success.')
