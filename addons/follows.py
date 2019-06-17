# coding: utf-8


import mitmproxy.http
from mitmproxy import ctx
import json
from item import item


class Follows:
    #用户发布的视频
    capture_user_post_url = "https://api.amemv.com/aweme/v1/aweme/post/?"
    #根据关键字搜索出来的用户
    capture_search_user_url = "https://api.amemv.com/aweme/v1/discover/search/?"


    def __init__(self):
        pass


    def response(self, flow: mitmproxy.http.flow):
        ctx.log.info(flow.request.url)
        if self.capture_user_post_url in flow.request.url:
            json_msg = json.loads(flow.response.text)
            aweme_list = json_msg['aweme_list'] if 'aweme_list' in json_msg else []
            item.aweme_list = aweme_list
            # ctx.log.debug(str(aweme_list))
            print(aweme_list)
        elif self.capture_search_user_url in flow.request.url:
            json_msg = json.loads(flow.response.text)
            user_list = json_msg['user_list'] if 'user_list' in json_msg else []
            item.user_list = user_list
            # ctx.log.debug(str(user_list))
            print(user_list)
        else:
            pass




addons = [
    Follows(),
]