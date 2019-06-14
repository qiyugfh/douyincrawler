# coding: utf-8

import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from addons.follows import Follows
from threading import Thread


'''
appium要做的事情是：
1、连接Genymotion模拟器中的抖音（版本6.6.0）
2、登陆抖音（抖音号Zsdxapp，登陆账号：18061675168/123456, 18901596648/abc123456）
3、搜索关键字，比如“南京工业大学”，得到下面的所有用户账号，点击关注这些账号
4、以后爬虫直接进入个人页，找到关注的所有账号，对这些账号进行爬视频
'''

'''
抖音6.6.6版本的主要元素ID：
主页  我   com.ss.android.ugc.aweme:id/wx
主页  发现  com.ss.android.ugc.aweme:id/kq
主页  发现   搜索框  com.ss.android.ugc.aweme:id/hp
搜索页 搜索框   com.ss.android.ugc.aweme:id/hn
搜索页 搜索按钮  com.ss.android.ugc.aweme:id/hp
用户列表中的关注按钮 com.ss.android.ugc.aweme:id/a9o
登陆页 	密码登陆 	com.ss.android.ugc.aweme:id/bpr
登陆页     请输入手机号码 com.ss.android.ugc.aweme:id/a5x
登陆页     输入账号密码	com.ss.android.ugc.aweme:id/a5w
登陆页		选中，我已阅读并同意用户协议和隐私政策 com.ss.android.ugc.aweme:id/bz9
登陆页 		确认	com.ss.android.ugc.aweme:id/nh
个人主页   关注 	com.ss.android.ugc.aweme:id/adw
'''


#连接模拟器
def init_driver():
    # 初始化配置，设置Desired Capabilities参数
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "5.1",
        # "udid": "192.168.186.104:5555",
        # "deviceName": "Samsung Galaxy S6",
        "udid": "9d5a33ea",
        "deviceName": "MI 4C",
        "appPackage": "com.ss.android.ugc.aweme",
        "appActivity": "com.ss.android.ugc.aweme.main.MainActivity",
        "unicodeKeyboard": True,
        "resetKeyboard": True,
        "noReset": True, #启动app时不要清除app里的原有的数据
        "newCommandTimeout": 600
    }
    # 指定Appium Server
    server = 'http://127.0.0.1:4723/wd/hub'
    # 新建一个Session
    driver = webdriver.Remote(server, desired_caps)
    driver.implicitly_wait(3)
    return driver

def home_page(driver):
    tabbars = []
    while True:
        try:
            tabbars = driver.find_elements_by_id('com.ss.android.ugc.aweme:id/cp7')
            if tabbars is not None and len(tabbars) == 5:
                break
        except Exception as e:
            print("当前页面不是主页面，等待中...")
            time.sleep(10)
    return tabbars



# 使用账号登陆
def account_login(driver):
    print('判断账户是否已经登陆')
    #在主界面点击“我”，进入'我的主页'
    tabbars = home_page(driver)
    print('点击主页中的"我"')
    tabbars[len(tabbars) - 1].click()
    time.sleep(10)
    #抖音号
    try:
        el0 = driver.find_element_by_id("com.ss.android.ugc.aweme:id/dcy")
        print('已经登陆')
        return
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


def tap_point(driver, x1, y1):
    print(driver.get_window_size())
    x0 = driver.get_window_size()['width']
    y0 = driver.get_window_size()['height']
    x2 = int(x1 * x0 / sw)
    y2 = int(y1 * y0 / sh)
    TouchAction(driver).tap(x=x2, y=y2).perform().release()
    time.sleep(5)


# 关注根据关键字搜出来的用户
def follow_user(driver):
    print('即将在首页根据关键搜索用户账号，并关注')
    #在主界面点击“首页”，进入'首页'
    tabbars = home_page(driver)
    print('点击主页中的"首页"')
    tabbars[0].click()
    time.sleep(10)
    # 点击首页的搜索按钮
    tap_point(driver, 990, 143)
    tap_point(driver, 362, 148)
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
            tap_point(driver, 450, 284)
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



# 我关注的账号
def my_follow_user(driver):
    print('即将进入我的关注页面')
    tabbars = home_page(driver)
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
            time.sleep()
    except Exception as e:
        print("获取我的关注中的用户列表出现异常")
        print(e)


def begin():
    # 建立驱动连接
    driver = init_driver()
    print("连接抖音app成功")
    account_login(driver)
    # 使用脚本执行之后，点击‘关注’过的用户，不知道为什么没有出现在‘我的关注’里，而手工点击‘关注’却可以
    # follow_user(driver)
    my_follow_user(driver)
    driver.quit()
    print("退出此次连接")


if __name__ != '__main__':
    exit(0)

# 以下是 main 函数内容



#测试账号
account = '18901596648'
password = 'abc123456'

#假设模拟器屏幕宽高：1080，1920
sw = 1080
sh = 1920


begin()
# thread = Thread(target=begin)
# thread.start()




