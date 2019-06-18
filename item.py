# coding: utf-8


class Item(object):
    crawler = 'appiumDouyin'
    crawlerName = '抖音'
    website = 'nufe-douyin'
    #抖音-昵称-抖音号
    name = '抖音-南京财经大学Mr zou-42514848'
    #抖音帐户ID
    url = '63564898194'
    periods = 1440
    query = 'nufe'
    user_list = []
    aweme_list = []


item = None
def getInstance():
    global item
    if item is None:
        item = Item()
        print("创建唯一实例的item")
    return item