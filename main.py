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
import logging


'''
此文件功能为：关注抖音账号
website: 学校的搜索关键字和相关信息配置
follows: 已关注的抖音号信息 
'''



class DouyinspiderSpider():

    def __init__(self, mSetting, appium_douyin):
        logger.info(('mongoSetting %s') % mSetting)
        self.name = "douyinSpider"
        self._client = pymongo.MongoClient(mSetting['url'])
        self._websites = self._client[mSetting['db']]['websites']
        self._accounts = self._client[mSetting['db']]['accounts']
        self._contents = self._client[mSetting['db']]['contents']
        self._appium_douyin = appium_douyin
        self._reqs = requests.session()
        self._reqs.keep_alive = False
        self._reqs.adapters.DEFAULT_RETRIES = 1000
        # websites表中的url
        self._ws = self._websites.find({'crawler': self.name, 'disabled': {'$exists': False}}, no_cursor_timeout = True).sort('time', 1)
        # self._ws = self._websites.find({'crawler': self.name, 'time':{'$exists': False}}, no_cursor_timeout=True)
        # self._ws = self._websites.find({'crawler': self.name, 'website':'douyin-977823453'}, no_cursor_timeout=True).sort('time', 1)
        # self._ws = self._websites.find({'crawler': self.name,
        #                           '$or': [{'query': {'$regex': 'xiaokanbiancheng'}}, {'query': {'$regex': 'chengxuyuandadui'}}, {'query': {'$regex': 'woshuodaima'}}]},
        #                          no_cursor_timeout=True).sort('time', -1)


    def follow_accounts(self):
        logger.info("开始执行自动化脚本，关注根据关键字搜索出来的用户")
        self._appium_douyin.search_input()
        now = time.time()
        for w in self.ws:
            if 'time' in w:
                if w['periods'] == 0:
                    logger.info('website %s not fetch !!!' % w['website'])
                    continue
                else:
                    if now < w['time'] + w['periods'] * 60:
                        logger.info('website %s not fetch because of time limit !!!' % w['website'])
                        continue
            self._appium_douyin.follow_user_list(w['url'])


            d = {}
            d['crawler'] = item.getInstance().crawler
            d['crawlerName'] = item.getInstance().crawlerName
            d['periods'] = w['periods']
            d['website'] = w['website']
            d['query'] = w['query']
            for user_info in item.getInstance().user_list:
                if 'user_info' not in user_info:
                    logging.warning("不是有效的用户信息")


                    continue
                d['url'] = user_info['user_info']['uid']
                d['name'] = "抖音-" + user_info['user_info']['nickname'] + "-" + user_info['user_info']['unique_id']
                d['time'] = time.time()
                logger.info("update account: %s" % d)
                self._accounts.update({'url': d['url']}, {'$setOnInsert': d}, True)
            self._websites.update_one({'website': w['website']}, {'$set': {'time': time.time()}})
            # 清空输入框，准备下个关键字的搜索
            self._appium_douyin.search_clear_input()
        self._ws.close()
        logger.info("执行关注用户的自动化脚本结束")

    def account_upsert(self, uid, nickname, unique_id):
        us =  self._accounts.find_one({'url': uid})
        if us is None:
            itm = item.Item()
            us = {}
            us['crawler'] = itm.crawler
            us['crawlerName'] = itm.crawlerName
            us['periods'] = itm.periods
            us['website'] = itm.website
            us['query'] = 'douyin'
            us['url'] = uid
            us['name'] = "抖音-" + nickname + "-" + unique_id
            us['time'] = time.time()
        logger.info("update account: %s" % us)
        self._accounts.update({'url': us['url']}, {'$setOnInsert': us}, True)
        return us

    def user_posts(self):
        for unique_id in self._appium_douyin.my_follow_user():
            aweme_list = item.getInstance().aweme_list
            logger.debug('===========user psot===========aweme_list : %s' % str(aweme_list))
            us = {}
            for aweme in aweme_list:
                if 'video' not in aweme:
                    logging.warning("没有视频信息")
                    continue
                user_id = aweme['author']['uid']
                nickname = aweme['author']['nickname']
                if len(us) == 0:
                    us = self.account_upsert(user_id, nickname, unique_id)
                self.content_upsert(aweme, us['crawlerName'], us['query'])

    def search_videos(self):
        logger.info("开始执行自动化脚本，爬取根据关键字搜索出来的视频")
        self._appium_douyin.search_input()
        for w in self._ws:
            for i in self._appium_douyin.search_videos(w['url']):
                if self.parse_content(w) is False:
                    continue
            self._websites.update_one({'website': w['website']}, {'$set': {'time': time.time()}})
        self._ws.close()
        logger.info("执行根据关键字搜索视频的自动化脚本结束")

    def search_videos_by_user_account(self):
        logger.info("开始执行自动化脚本，爬取根据关键字搜索用户主页人里的视频")
        self._appium_douyin.search_input()
        for w in self._ws:
            if self._appium_douyin.search_videos_by_user_account(w['url']) is False:
                continue
            if self.parse_content(w) is False:
                continue
            self._websites.update_one({'website': w['website']}, {'$set': {'time': time.time()}})
        self._ws.close()
        logger.info("执行根据关键字搜索用户视频的自动化脚本结束")

    def parse_content(self, w):
        try:
            aweme_list = item.getInstance().aweme_list
            logger.debug('===========user search===========aweme_list : %s' % str(aweme_list))
            for aweme in aweme_list:
                if 'video' not in aweme:
                    logging.warning("没有视频信息")
                    return False
                self.content_upsert(aweme, w['crawlerName'], w['query'])
        except Exception as e:
            logging.error("抓取视频失败")
            return False
        return True

    def content_upsert(self, aweme, crawlerName, query):
        d = {}
        d['crawlerName'] = crawlerName
        d['module'] = "抖音视频"
        website = query + '-' if len(query) > 0 else ''
        d['website'] = 'douyin-' + website + aweme['author']['uid']
        unique_id = aweme['author']['unique_id'] if len(aweme['author']['unique_id']) > 0 else aweme['author']['short_id']
        d['websiteName'] = '抖音-' + aweme['author']['nickname'] + '-' + unique_id
        d['title'] = ''
        d['query'] = query
        d['time'] = aweme['create_time'] * 1.0 if 'create_time' in aweme else time.time()
        d['id'] = aweme['aweme_id']
        d['imageUrls'] = []
        d['body'] = aweme['desc']
        d['sourceBody'] = aweme
        # 读取视频uri
        video_uri = aweme['video']['play_addr']['uri']
        # 拼接视频地址
        video = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=" + video_uri
        d['videoUrls'] = [video]
        d['url'] = video
        d['crawlTime'] = time.time()
        logger.info("update content: %s" % str(d))
        self._contents.update({'id':d['id'], 'website': d['website'], 'url': d['url']}, {'$setOnInsert': d}, True)
        self.postItem(d)


    def postItem(self, d):
        url = "http://192.168.1.31:1528/crawler"
        data = {'json' : json.dumps(d)}
        response = self._reqs.post(url=url, data=data)
        if response is None or response.json()['status'] != 0:
            logger.error("post json to 1.31 fail ...")


def begin():
    logger.info('自动化采集抖音视频的脚本开始执行')
    appium_driver = AppiumDriver()
    appium_douyin = AppiumDouyin(appium_driver)
    spider = DouyinspiderSpider(mSetting, appium_douyin)
    if appium_douyin.account_login() is not True:
        logger.info("账户没有登陆，退出执行")
        exit(0)
    # 关注根据关键字搜索出来的抖音账户
    # spider.follow_accounts()
    # 爬取已关注的抖音账户下的视频
    # spider.user_posts()
    # 爬取根据关键字搜索出来的抖音视频
    # spider.search_videos()
    # 爬取根据关键字搜索出来的用户主页的视频
    spider.search_videos_by_user_account()
    appium_driver.quit()



def init_logger():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT,
                        datefmt='%m-%d %H:%M')
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console = logging.FileHandler(filename='appium_douyin.log', mode='w', encoding='utf-8')
    console.setLevel(logging.INFO)
    # 设置日志打印格式
    formatter = logging.Formatter(LOG_FORMAT)
    console.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('appiumDouyin').addHandler(console)


'''
main 函数开始
'''
init_logger()

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

logger = logging.getLogger('appiumDouyin')





# begin()
thread = Thread(target=begin)
thread.start()

logger.info('已启动线程进行处理')

