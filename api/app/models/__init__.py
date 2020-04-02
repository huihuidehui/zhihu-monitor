from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.model import Question, Answer, User, FollowerNum, ViewNum, LikeNums, CollectNums, CommentNum, VoteNum, \
    Rank
