# coding: utf-8


import mitmproxy.http
import json
import item



class Follows:

    def __init__(self):
        # 用户发布的视频
        self._capture_user_post_url = "https://api.amemv.com/aweme/v1/aweme/post/?"
        # 根据关键字搜索出来的用户
        self._capture_search_user_url = "https://api.amemv.com/aweme/v1/discover/search/?"


    def response(self, flow: mitmproxy.http.HTTPFlow) -> None:
        if flow.request.url.startswith(self._capture_user_post_url):
            print("捕捉到的用户主界面的http请求url: %s" % flow.request.url)
            print("捕捉到的用户主界面的http请求响应text: %s" % flow.request.url)
            json_msg = json.loads(flow.response.text)
            aweme_list = json_msg['aweme_list'] if 'aweme_list' in json_msg else []
            item.getInstance().aweme_list = aweme_list
            print("用户发布的作品: %s" % str(aweme_list))
        elif flow.request.url.startswith(self._capture_search_user_url):
            print("捕捉到的用户搜索的http请求url: %s" % flow.request.url)
            print("捕捉到的用户搜索的http请求响应text: %s" % flow.response.text)
            json_msg = json.loads(flow.response.text)
            user_list = json_msg['user_list'] if 'user_list' in json_msg else []
            item.getInstance().user_list = user_list
            print("用户搜索结果: %s" % str(user_list))
        else:
            pass

