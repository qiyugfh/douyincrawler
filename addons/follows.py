# coding: utf-8


import mitmproxy.http
from mitmproxy import ctx
import json
import time


class Follows:
    capture_url = "https://api.amemv.com/aweme/v1/aweme/post/?max_cursor=0&user_id="

    def __init__(self):
        pass

    def response(self, flow: mitmproxy.http.flow):
        ctx.log.info(flow.request.url)
        if self.capture_url in flow.request.url:
            json_msg = json.loads(flow.response.text)
            aweme_list = json_msg['aweme_list'] if 'aweme_list' in json_msg else []


addons = [
    Follows(),
]