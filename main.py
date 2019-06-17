# -*- coding: utf-8 -*-

import time
import pymongo
from appium_douyin import AppiumDouyin
from item import item
import json
from threading import Thread


'''
此文件功能为：关注抖音账号
website: 学校的搜索关键字和相关信息配置
follows: 已关注的抖音号信息 
'''


class DouyinspiderSpider():

    def __init__(self, mSetting):
        print(('mongoSetting %s') % mSetting)
        self.name = "douyinSpider"
        self.client = pymongo.MongoClient(mSetting['url'],
                                          username=mSetting['name'],
                                          password=mSetting['password'],
                                          authSource=mSetting['authDB'])
        self.websites = self.client[mSetting['db']]['websites']
        self.account = self.client[mSetting['db']]['account']
        self.contents = self.client[mSetting['db']]['contents']


    def follow_accounts(self):
        print("开始执行自动化脚本，关注根据关键字搜索出来的用户")
        appium_douyin.search_input()
        now = time.time()
        #websites表中的url
        ws = self.websites.find({'crawler': self.name}, no_cursor_timeout = True)
        for w in ws:
            # if 'time' in w:
            #     if w['periods'] == 0:
            #         print('website %s not fetch !!!' % w['website'])
            #         continue
            #     else:
            #         if now < w['time'] + w['periods'] * 60:
            #             print('website %s not fetch because of time limit !!!' % w['website'])
            #             continue
            appium_douyin.follow_user(w['url'])
            d = {}
            d['crawler'] = item.crawler
            d['crawlerName'] = item.crawlerName
            d['periods'] = item.periods
            d['website'] = item.website
            d['query'] = item.query
            for user_info in item.user_list:
                d['url'] = user_info['userInfo']['uid']
                d['name'] = "抖音-" + user_info['nickname'] + "-" + user_info['userInfo']['unique_id']
                print("update account: %s" % d)
                self.account.update({'url': d['url']}, {'$setOnInsert': d}, True)
            self.websites.update_one({'website': w['website']}, {'$set': {'time': time.time()}})
            # 清空输入框，准备下个关键字的搜索
            appium_douyin.search_clear_input()
        ws.close()
        print("执行关注用户的自动化脚本结束")


    def user_posts(self):
        for unique_id in appium_douyin.my_follow_user():
            d = {}
            user_id = aweme['author']['uid']
            us = self.account.find({'url' : user_id})
            if us is None or len(us) != 1:
                continue
            d['crawlerName'] = us['crawlerName']
            d['module'] = "抖音视频"
            d['website'] = us['website']
            d['websiteName'] = us['name']
            d['title'] = ''
            d['query'] = us['query']
            for aweme in item.aweme_list:
                d['time'] = aweme['create_time'] * 1.0 if 'create_time' in aweme else time.time()
                d['id'] = aweme['aweme_id']
                d['images'] = []
                d['body'] = aweme['desc']
                d['sourceBody'] = aweme
                # 读取视频uri
                video_uri = aweme['video']['play_addr']['uri']
                # 拼接视频地址
                video = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=" + video_uri
                d['videos'] = [{"url": video}]
                d['url'] = video
                print("update content: %s" % d)
                self.contents.update({'website': d['website'], 'url': d['url']}, {'$setOnInsert': d}, True)
                self.postItem(d)


    def postItem(self, d):
        url = "http://192.168.1.31:528/crawler"
        data = {'json' : json.dumps(d)}
        response = self.reqs.post(url=url, data=data)
        if response is None or response.json()['status'] != 0:
            print("post json to 1.31 fail ...")



def begin():
    if appium_douyin.account_login() is not True:
        print("账户没有登陆，退出执行")
        exit(0)
    spider.follow_accounts()
    # spider.user_posts()



if __name__ != "__main__":
    exit(1)


mSetting = {
   "url": "mongodb://localhost:27017/",
   "name": 'root',
   "password": '123456',
   "authDB": 'admin',
   "db": 'douyin'
}

spider = DouyinspiderSpider(mSetting)
appium_douyin = AppiumDouyin()

begin()

#
# thread = Thread(target=begin)
# thread.start()