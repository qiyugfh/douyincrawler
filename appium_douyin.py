# coding: utf-8

import time
from addons.follows import Follows
from threading import Thread
from appium_driver import driver

'''
appium要做的事情是：
1、连接Genymotion模拟器（或手机）中的抖音app（版本6.6.0）
2、登陆抖音（抖音号Zsdxapp，登陆账号：18061675168/123456, 18901596648/abc123456）
3、搜索关键字，比如“南京工业大学”，得到下面的所有用户账号，点击关注这些账号
4、以后爬虫直接进入个人页，找到关注的所有账号，对这些账号进行爬视频
'''



def home_page():
    tabbars = []
    while True:
        try:
            #主页下方的导航
            tabbars = driver.find_elements_by_id('com.ss.android.ugc.aweme:id/cp7')
            if tabbars is not None and len(tabbars) == 5:
                break
        except Exception as e:
            print("当前页面不是主页面，等待中...")
            time.sleep(10)
    return tabbars



# 使用账号登陆
def account_login():
    print('判断账户是否已经登陆')
    #在主界面点击“我”，进入'我的主页'
    tabbars = home_page()
    print('点击主页中的"我"')
    tabbars[len(tabbars) - 1].click()
    time.sleep(10)
    #抖音号
    try:
        el0 = driver.find_element_by_id("com.ss.android.ugc.aweme:id/dcy")
        if '抖音号' in el0.text:
            print('已经登陆')
    except Exception as e:
        print("账号未登陆，即将登陆")
        try:
            #点击密码登陆
            el0 = driver.find_element_by_id("com.ss.android.ugc.aweme:id/bpr")
            el0.click()
            time.sleep(2)
            #账号
            el1 = driver.find_element_by_id("com.ss.android.ugc.aweme:id/a5x")
            el1.send_keys(account)
            time.sleep(2)
            #密码
            el2 = driver.find_element_by_id("com.ss.android.ugc.aweme:id/a5w")
            el2.send_keys(password)
            time.sleep(5)
            #同意协议
            driver.find_element_by_id("com.ss.android.ugc.aweme:id/bz9").click()
            time.sleep(2)
            #登陆
            driver.find_element_by_id("com.ss.android.ugc.aweme:id/nh").click()
            time.sleep(60)
        except Exception as e:
            print("账户密码登陆出现异常")
            print(e)
            return False
    return True


# 关注根据关键字搜出来的用户
def follow_user():
    print('即将在首页根据关键搜索用户账号，并关注')
    #在主界面点击“首页”，进入'首页'
    tabbars = home_page()
    print('点击主页中的"首页"')
    tabbars[0].click()
    time.sleep(10)
    # 点击首页的搜索按钮
    driver.tap_point(990, 143)
    driver.tap_point(362, 148)
    try:
        # keywords = ['南京财经大学', '南京航空航天大学', '南京工业大学', '东南大学', '南京邮电大学']
        keywords = ['南京财经大学']
        for keyword in keywords:
            print(("搜索关键字：%s" % keyword))
            # 输入关键字，点击搜索
            driver.find_element_by_id("com.ss.android.ugc.aweme:id/a8g").send_keys(keyword)
            driver.find_element_by_id("com.ss.android.ugc.aweme:id/d7r").click()
            time.sleep(2)
            # 切换到用户的tab页
            driver.tap_point(450, 284)
            # 点击所有的关注按钮
            els = driver.find_elements_by_id("com.ss.android.ugc.aweme:id/n2")
            print("获取搜索到的关注按钮个数：%s" % len(els))
            for el in els:
                if el.text == "关注":
                    el.click()
                    time.sleep(3)
            # 删除搜索框的内容，准备下一次搜索
            driver.find_element_by_id("com.ss.android.ugc.aweme:id/mq").click()
    except Exception as e:
        print("根据关键字搜索用户出现异常")
        print(e)
        return False
    return True


# 我关注的账号
def my_follow_user():
    print('即将进入我的关注页面')
    tabbars = home_page()
    print('点击主页中的"我"')
    tabbars[len(tabbars) - 1].click()
    time.sleep(10)
    print('点击"我"中的"关注"')
    try:
        driver.find_element_by_id('com.ss.android.ugc.aweme:id/adw').click()
        time.sleep(10)
        user_els = driver.find_elements_by_id("com.ss.android.ugc.aweme:id/au3")
        for use_el in user_els:
            use_el.click()
            time.sleep(3)
    except Exception as e:
        print("获取我的关注中的用户列表出现异常")
        print(e)
        return False
    return True


def begin():
    # 建立驱动连接
    print("连接抖音app成功")
    account_login()
    # 使用脚本执行之后，点击‘关注’过的用户，不知道为什么没有出现在‘我的关注’里，而手工点击‘关注’却可以
    # follow_user(driver)
    my_follow_user()
    print("退出此次连接")


if __name__ != '__main__':
    exit(0)

'''
以下是 main 函数内容
'''

#测试账号
account = '18901596648'
password = 'abc123456'

begin()

# thread = Thread(target=begin)
# thread.start()




