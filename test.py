# coding: utf-8


import re
import logging
import hashlib
import requests
import os
import time
import urllib.parse

key='南京大学'
headers = {'User-Agent' : 'com.ss.android.ugc.aweme/630 (Linux; U; Android 9; zh_CN; ONEPLUS A5010; Build/PKQ1.180716.001; Cronet/58.0.2991.0)'}
url="https://api-hl.amemv.com/aweme/v1/general/search/single/?ts=1558682232&js_sdk_version=&app_type=normal&manifest_version_code=630&_rticket=1558682231941&ac=wifi&device_id=46703154728&iid=73208755099&mcc_mnc=46011&os_version=9&channel=oppo&version_code=630&device_type=ONEPLUS%%20A5010&language=zh&uuid=99001155132222&resolution=1080*2034&openudid=a6ea9a05367b2f92&update_version_code=6302&app_name=aweme&version_name=6.3.0&os_api=28&device_brand=OnePlus&ssmix=a&device_platform=android&dpi=420&aid=1128&offset=0&count=10&is_pull_refresh=0&search_source=search_history&hot_search=0&latitude=0.0&longitude=0.0&search_id=&query_correct_type=1&keyword=" + urllib.parse.quote(key)

i = 0
while True:
	i = i+1
	print("-------------------- i = ", i)
	response = requests.post(url=url, headers=headers)
	if response is None:
		continue
	json_str = response.json()
	print('-------------------- json_str = ', json_str)
    aweme_list = json_str['data'] if 'data' in json_str else []
	if len(aweme_list) > 0:
		break