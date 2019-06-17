# coding: utf-8

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time


#连接模拟器或者android手机
class AppiumDriver:

    # 假设模拟器屏幕宽高：1080，1920
    def __init__(self, _sw = 1080, _sh = 1920):
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
            "noReset": True,  # 启动app时不要清除app里的原有的数据
            "newCommandTimeout": 600
        }
        # 指定Appium Server
        server = 'http://127.0.0.1:4723/wd/hub'
        # 新建一个Session
        self._driver = webdriver.Remote(server, desired_caps)
        self._driver.implicitly_wait(3)
        print("连接抖音app成功")
        print('success ...')

    def __del__(self):
        self._driver.quit()
        print("退出此次连接")


    def tap_point(self, x1, y1):
        print(self._driver.get_window_size())
        x0 = self._driver.get_window_size()['width']
        y0 = self._driver.get_window_size()['height']
        x2 = int(x1 * x0 / self._sw)
        y2 = int(y1 * y0 / self._sh)
        TouchAction(self._driver).tap(x = x2, y = y2).perform().release()
        time.sleep(5)


    def find_element_by_id(self, id):
        el = self._driver.find_element_by_id(id)
        return el


    def find_elements_by_id(self, id):
        els = self._driver.find_element_by_id(id)
        return els


    def get_driver(self):
        return self._driver





driver = AppiumDriver()
