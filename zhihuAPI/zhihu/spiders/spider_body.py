# -*- coding: UTF-8 -*-
import scrapy
import os
import random, time
import json
from scrapy.selector import Selector
from zhihuAPI.zhihu.items import ZhihuapiItem

class zhihuSpider(scrapy.Spider):
    name = "zhihu"

    user_name = 'email'
    password = 'password'
    xsrf_token = ''

    topic_url = 'topic url you want to crawl'
    user_agents = []
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.zhihu.com/",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    }

    login_url = 'https://www.zhihu.com/'
    signin_url = 'https://www.zhihu.com/login/email'

    #starting point for the spider
    #getting the xsrf token (its unique for every login.)
    def start_requests(self):

        # self.user_name = input('Input ur username...\n')
        # self.password = input('Input ur password...\n')
        # self.topic_url = input('Topic url you want to search...\n')

        #assign user agents
        self.user_agents = self.get_user_agents()
        self.logger.info('current user agent: {}'.format(self.user_agents))

        return [
            scrapy.http.FormRequest(
                self.login_url,
                headers = self.headers,

                #cookies = self.cookies,
                callback = self.post_login
            )
        ]

    def post_login(self, response):
        self.xsrf_token = response.xpath('//input[@name = "_xsrf"]/@value').extract_first()
        self.logger.info('xsrf token for current login: {}'.format(self.xsrf_token))

        # assign a random user agents
        self.headers['user-agent'] = self.user_agents[0]
        self.headers['X-Xsrftoken'] = self.xsrf_token

        #send username and password along with xsrf token to server.
        return [
            scrapy.http.FormRequest(
            self.signin_url,
            method = 'POST',
            headers = self.headers,
            formdata = {
                '_xsrf': self.xsrf_token,
                'password': self.password,
                'captcha_type': 'cn',
                'email': self.user_name
            },
            callback=self.after_login
        )]

    def after_login(self, response):
        login_info = json.loads(response.body.decode("utf-8"))

        self.logger.info('sign info: {}'.format(login_info['msg']))

        if int(login_info['r']) == 0:
            #sign in successfully
            yield scrapy.http.FormRequest(
                self.topic_url,
                method = 'POST',
                headers = self.headers,
                formdata = {
                    'start': '0'
                },
                callback = self.parse
            )

        elif int(login_info['r']) == 1:
            #sign in failed
            self.logger.error('sign in failed with error message: {}'.format(login_info['data']))
            randomtime = str(int(time.time() * 1000))
            captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + \
                         randomtime + "&type=login"
            yield scrapy.Request(
                url = captchaurl,
                method = 'GET',
                headers = self.headers,
                callback = self.handle_captcha
            )

    #handle failed login due to captcha test - compeletely automated public turning test to tell computers and humans apart.
    def handle_captcha(self, response):
        with open('checkcode.gif', 'wb') as f:
            f.write(response.body)
            f.close()
        os.system('open checkcode.gif')
        captcha = input('请输入验证码：')
        print(captcha)

        yield scrapy.http.FormRequest(
            self.signin_url,
            method='POST',
            headers=self.headers,
            formdata={
                '_xsrf': self.xsrf_token,
                'password': self.password,
                'captcha': captcha,
                'email': self.user_name
            },
            callback=self.after_login
        )

    #after successfully login, starting handle the actual content.
    def parse(self, response):
        #getting the question blocks from response.
        question_blocks = Selector(text=json.loads(response.body.decode("utf-8"))['msg'][1]).xpath('//div[contains(@itemtype, "http://schema.org/Question")]')

        for question_block in question_blocks:
            item = ZhihuapiItem()
            item['question_name'] = question_block.xpath('.//div/div/h2/a/text()').extract_first()
            item['question_url'] = question_block.xpath('.//div/div/h2/a/@href').extract_first()
            print ("question: ", question_block.xpath('.//div/div/h2/a/text()').extract_first())

        last_data_score = question_blocks[len(question_blocks)-1].xpath('@data-score').extract_first()

        print ("last data score ", last_data_score)
        yield scrapy.http.FormRequest(
            self.topic_url,
            method='POST',
            headers=self.headers,
            formdata={
                'start': '0',
                'offset': str(last_data_score)
            },
            callback=self.parse
        )

    #read user agents from file.
    def get_user_agents(self):
        self.logger.info('we are getting user agents...')
        with open("%s/zhihu/user_agents.txt" % os.getcwd()) as user_agent_file:
            user_agents = user_agent_file.read().split("\n")
        return user_agents