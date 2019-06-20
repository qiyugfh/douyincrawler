# coding: utf-8


import mitmproxy.http
import json
import item
import logging

logger = logging.getLogger('appiumDouyin')


class Follows:

    def __init__(self):
        # 用户发布的视频
        self._capture_user_post_url = "https://api.amemv.com/aweme/v1/aweme/post/?"
        # 根据关键字搜索出来的用户
        self._capture_search_user_url = "https://api.amemv.com/aweme/v1/discover/search/?"
        self._ua = 'com.ss.android.ugc.aweme/630 (Linux; U; Android 9; zh_CN; ONEPLUS A5010; Build/PKQ1.180716.001; Cronet/58.0.2991.0)'


    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.headers['User-Agent']:
            flow.request.headers['User-Agent'] = self._ua


    def response(self, flow: mitmproxy.http.HTTPFlow) -> None:
        if flow.request.url.startswith(self._capture_user_post_url):
            logger.info("捕捉到的用户主界面的http请求url: %s" % flow.request.url)
            logger.info("捕捉到的用户主界面的http请求响应text: %s" % flow.request.url)
            json_msg = json.loads(flow.response.text)
            aweme_list = json_msg['aweme_list'] if 'aweme_list' in json_msg else []
            item.getInstance().aweme_list = aweme_list
            logger.info("用户发布的作品: %s" % str(aweme_list))
        elif flow.request.url.startswith(self._capture_search_user_url):
            logger.info("捕捉到的用户搜索的http请求url: %s" % flow.request.url)
            logger.info("捕捉到的用户搜索的http请求响应text: %s" % flow.response.text)
            json_msg = json.loads(flow.response.text)
            user_list = json_msg['user_list'] if 'user_list' in json_msg else []
            item.getInstance().user_list = user_list
            logger.info("用户搜索结果: %s" % str(user_list))
        else:
            pass

