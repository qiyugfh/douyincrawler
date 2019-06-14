# -*- coding: utf-8 -*-

import time
import pymongo
import logging



'''
此文件功能为关注抖音账号
website: 学校的搜索关键字和相关信息配置
follows: 已关注的抖音号信息 
'''

class DouyinspiderSpider():

    def __init__(self, mSetting):
        logging.info(('mongoSetting %s') % mSetting)
        self.name = "douyinSpider"
        self.client = pymongo.MongoClient(mSetting['url'],
                                          username=mSetting['name'],
                                          password=mSetting['password'],
                                          authSource=mSetting['authDB'])
        self.collection = self.client[mSetting['db']]['websites']
        self.contents = self.client[mSetting['db']]['contents']


    def start_requests(self):
        now = time.time()
        ws = self.collection.find({'crawler': self.name}, no_cursor_timeout = True)
        for w in ws:
            if 'time' in w:
                if w['periods'] == 0:
                    logging.warning('website %s not fetch !!!' % w['website'])
                    continue
                else:
                    if now < w['time'] + w['periods'] * 60:
                        logging.warning('website %s not fetch because of time limit !!!' % w['website'])
                        continue
            # douyin = Douyin(w)
            # items = douyin.do_request()
            # if items:
            #     # self.insert_update_contents(items)
            #     self.collection.update_one({'website': w['website']}, {'$set': {'time': time.time()}})
        ws.close()


    def insert_update_contents(self, items):
        for item in items:
            data = dict(item)
            logging.info("update contents: %s" % data)
            self.contents.update({'website': data['website'], 'websiteName': data['websiteName'], 'id': data['id']}, {'$setOnInsert': data}, True)



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
spider.start_requests()

logging.info("download over !!!")