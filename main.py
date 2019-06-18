# coding: utf-8

import time
import pymongo
from appium_driver import AppiumDriver
from appium_douyin import AppiumDouyin
import item
import json
from threading import Thread
import requests
from addons.follows import Follows


'''
此文件功能为：关注抖音账号
website: 学校的搜索关键字和相关信息配置
follows: 已关注的抖音号信息 
'''



class DouyinspiderSpider():

    def __init__(self, mSetting, appium_douyin):
        print(('mongoSetting %s') % mSetting)
        self.name = "douyinSpider"
        self._client = pymongo.MongoClient(mSetting['url'])
        self._websites = self._client[mSetting['db']]['websites']
        self._account = self._client[mSetting['db']]['account']
        self._contents = self._client[mSetting['db']]['contents']
        self._appium_douyin = appium_douyin
        self._reqs = requests.session()
        self._reqs.keep_alive = False
        self._reqs.adapters.DEFAULT_RETRIES = 1000


    def follow_accounts(self):
        print("开始执行自动化脚本，关注根据关键字搜索出来的用户")
        self._appium_douyin.search_input()
        now = time.time()
        #websites表中的url
        ws = self._websites.find({'crawler': self.name}, no_cursor_timeout = True)
        for w in ws:
            # if 'time' in w:
            #     if w['periods'] == 0:
            #         print('website %s not fetch !!!' % w['website'])
            #         continue
            #     else:
            #         if now < w['time'] + w['periods'] * 60:
            #             print('website %s not fetch because of time limit !!!' % w['website'])
            #             continue
            self._appium_douyin.follow_user_list(w['url'])
            d = {}
            d['crawler'] = item.getInstance().crawler
            d['crawlerName'] = item.getInstance().crawlerName
            d['periods'] = item.getInstance().periods
            d['website'] = item.getInstance().website
            d['query'] = item.getInstance().query
            for user_info in item.getInstance().user_list:
                d['url'] = user_info['user_info']['uid']
                d['name'] = "抖音-" + user_info['user_info']['nickname'] + "-" + user_info['user_info']['unique_id']
                print("update account: %s" % d)
                self._account.update({'url': d['url']}, {'$setOnInsert': d}, True)
            self._websites.update_one({'website': w['website']}, {'$set': {'time': time.time()}})
            # 清空输入框，准备下个关键字的搜索
            self._appium_douyin.search_clear_input()
        ws.close()
        print("执行关注用户的自动化脚本结束")


    def user_posts(self):
        for unique_id in self._appium_douyin.my_follow_user():
            aweme_list = item.getInstance().aweme_list
            print('aweme_list : %s' % str(aweme_list))
            for aweme in aweme_list:
                d = {}
                user_id = aweme['author']['uid']
                us = self._account.find_one({'url': user_id})
                if us is None:
                    us = {}
                    us['query'] = 'unkown'
                d['crawlerName'] = '抖音'
                d['module'] = "抖音视频"
                d['website'] =  us['query'] + '-douyin-' + user_id
                d['websiteName'] = '抖音-' + aweme['author']['nickname'] + '-' + aweme['author']['unique_id']
                d['title'] = ''
                d['query'] = us['query']
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
                print("update content: %s" % str(d))
                self._contents.update({'website': d['website'], 'url': d['url']}, {'$setOnInsert': d}, True)
                # self.postItem(d)


    def postItem(self, d):
        url = "http://192.168.1.31:528/crawler"
        data = {'json' : json.dumps(d)}
        response = self._reqs.post(url=url, data=data)
        if response is None or response.json()['status'] != 0:
            print("post json to 1.31 fail ...")


def begin():
    appium_driver = AppiumDriver()
    appium_douyin = AppiumDouyin(appium_driver)
    spider = DouyinspiderSpider(mSetting, appium_douyin)
    if appium_douyin.account_login() is not True:
        print("账户没有登陆，退出执行")
        exit(0)
    # spider.follow_accounts()
    spider.user_posts()
    # appium_driver.quit()


print('自动化采集抖音视频的脚本开始执行')

mSetting = {
   "url": "mongodb://127.0.0.1:27017/",
   "name": 'root',
   "password": '123456',
   "authDB": 'admin',
   "db": 'douyin'
}

addons = [
    Follows(),
]

# begin()


thread = Thread(target=begin)
thread.start()

print('\n已启动线程进行处理')
