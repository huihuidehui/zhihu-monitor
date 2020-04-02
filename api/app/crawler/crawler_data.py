#!/usr/bin/env python
# encoding: utf-8
import json
import requests
import time

from flask import current_app
from lxml import etree
import random


class ZhSpider(object):

    def __init__(self):
        """
        :param question_id: 问题ID，列表形式
        :param min_voted_num: 将会过滤掉点赞数小于这个值得回答

        """

        self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-us",
                        "Connection": "keep-alive",
                        "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}
        self.question_base_url = "https://www.zhihu.com/question/{}"

        self.answer_base_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={}&offset=0&platform=desktop&sort_by=default"

    def start(self):
        """
        启动爬虫
        """
        pass

    def get_follower_view_title(self, question_id):
        """
        根据问题id返回该问题的关注数和浏览数和标题
        :param question_id: 问题id
        :return: follower_num, view_num
        """
        url = self.question_base_url.format(question_id)
        response = self.get(url)
        # 使用xpath获取关注数和浏览数
        html = etree.HTML(response.text)
        follower_num, view_num = html.xpath('//strong[@class="NumberBoard-itemValue"]/text()')
        follower_num, view_num = int(follower_num.replace(',', '')), int(view_num.replace(',', ''))
        title = html.xpath('//h1[@class="QuestionHeader-title"]/text()')[0]
        return follower_num, view_num, title

    def get(self, url):
        """
        get请求
        :param url:
        :return:
        """
        # response = requests.get(url, proxies={'http': random.choice(current_app.config['IPS'])}, headers=self.headers)
        response = requests.get(url, headers=self.headers)
        time.sleep(1)
        return response

    def get_answer_data(self, answer_name, question_id):
        """
        根据回答者name爬去信息
        :param answer_name:
        :return: 赞同数，评论数,排名
        """
        answer_url = self.answer_base_url.format(question_id, 5)
        next_page_answer_url = answer_url
        rank = 0
        vote_num = 0
        comment_num = 0
        is_found = False
        while next_page_answer_url is not None:
            response = self.get(next_page_answer_url)
            answers_dic_data = json.loads(response.content.decode('utf8'))
            for answer in answers_dic_data.get('data'):
                rank += 1
                if answer.get('author').get('name') == answer_name:
                    # 记录数据
                    vote_num = answer.get('voteup_count')
                    comment_num = answer.get('comment_count')
                    is_found = True
                    break
            if is_found:
                # 跳出循环
                break
            if not answers_dic_data.get('paging').get('is_end'):
                # 下一页
                next_url = answers_dic_data.get('paging').get('next')
                next_page_answer_url = next_url
            else:
                # 没有找到回答
                next_page_answer_url = None
        return vote_num, comment_num, rank
